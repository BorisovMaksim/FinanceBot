from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.node_parser import SimpleNodeParser
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import re

PROMT = "Ответь на вопрос: {query_str}"

SP = """Ты умный ассистент которого зовут Финансист. 
Отвечай как человек, который разбирается в финансах. Если ты не знаешь ответа, ответь не знаю. Отвечай кратко (можешь шутливо), не более 1 предложения."""

MODEL_NAME = "IlyaGusev/saiga2_7b_lora"

DEVICE = "cuda:2"


def create_nodes():
    documents = SimpleDirectoryReader("data").load_data()
    parser = SimpleNodeParser.from_defaults(
        separator="\n", chunk_size=256, chunk_overlap=32
    )
    nodes = parser.get_nodes_from_documents(documents, show_proggres=True)
    len(nodes)

    for node in nodes:
        node.text = re.sub("\\n", " ", node.text)
        node.text = re.sub(" +", " ", node.text)
    return nodes


def init_model():
    nodes = create_nodes()
    config = PeftConfig.from_pretrained(MODEL_NAME)
    llm = AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        torch_dtype=torch.float16,
        load_in_8bit=False,
        device_map=DEVICE,
        cache_dir="/data/vdimitrov/rag/.cache",
    )
    llm_for_peft = PeftModel.from_pretrained(llm, MODEL_NAME, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        # bnb_4bit_compute_dtype=torch.int8,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    llm = HuggingFaceLLM(
        model=llm,
        tokenizer=tokenizer,
        context_window=4096,
        max_new_tokens=256,
        generate_kwargs={"temperature": 0.3, "do_sample": True},
        query_wrapper_prompt=PROMT,
        system_prompt=SP,
        device_map=DEVICE,
        tokenizer_kwargs={"max_length": 4096},
        model_kwargs={"quantization_config": quantization_config}
        # model_kwargs={"torch_dtype": torch.int8},
    )
    service_context = ServiceContext.from_defaults(
        chunk_size=256, llm=llm, embed_model="local:cointegrated/LaBSE-en-ru"
    )
    index = VectorStoreIndex(nodes=nodes, service_context=service_context)
    return index, llm


def response(question, index):
    query_engine = index.as_query_engine(similarity_top_k=5)
    res = query_engine.query(question)
    return res.response
