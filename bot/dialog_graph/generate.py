from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch

 
MODEL_NAME = "IlyaGusev/saiga2_7b_lora"

DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"

DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"

SP = "Ты финансовый ассистент. Ты любишь давать рекомендации по поводу улучшения инвестиционного портфеля."

GENERATION_CONFIG = GenerationConfig.from_pretrained(MODEL_NAME)

DEVICE = "cuda:0"


def init_model():
    config = PeftConfig.from_pretrained(MODEL_NAME)
    llm = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            torch_dtype=torch.float16,
            load_in_8bit=True,
            device_map="cuda:0",
        )
    llm = PeftModel.from_pretrained(llm, MODEL_NAME, torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    return llm, tokenizer


def generate(model, tokenizer, prompt):
    data = tokenizer(prompt, return_tensors="pt")
    data = {k: v.to(DEVICE) for k, v in data.items()}
    output_ids = model.generate(**data, generation_config=GENERATION_CONFIG)[0]
    output_ids = output_ids[len(data["input_ids"][0]) :]
    output = tokenizer.decode(output_ids, skip_special_tokens=True)
    return output.strip()


def get_prompt(messages):
    final_text = ""
    for message in messages:
        message_text = DEFAULT_MESSAGE_TEMPLATE.format(**message)
        final_text += message_text
    final_text += DEFAULT_RESPONSE_TEMPLATE
    return final_text.strip()


def response(prompt, llm, tokenizer):
    messages = [{"role": "system", "content": SP, "role": "user", "content": prompt}]
    prompt = get_prompt(messages)
    output = generate(llm, tokenizer, prompt)
    return output


def risk_profile(
    llm,
    tokenizer, 
    invest_goals,
    duration,
    funds_volume,
    daily_expenses,
    is_risky,
    invest_experience,
    capital_reduction,
    early_withdrawal,
    reserve_fund,
    private_property,
    retirement,
    monthly_income_expenses,
    debt_obligation,
    age,
):
    prompt = f"Есть риск-профиль для конкретного инвестора со следущими критериям: цели инвестирования - {invest_goals}, \
    срок инвестирования - {duration} лет, объем финансовых активовов для инвестирования - {funds_volume} рублей, планируется ли использовать \
    инвестируемые средства для финансирования ежедневных \
    расходов - {daily_expenses}, есть ли готовность принимать более высокий риск для достижения более высокого потенциального прироста - {is_risky}, \
    наличие опыта в качестве инвестора - {invest_experience}, \
    есть ли готовность к возможности снижения инвестиционного капитала - {capital_reduction}, вероятность изъятия большей части или всей инвестированной суммы досрочно, \
    до истечения предполагаемого срока инвестиций - {early_withdrawal}, есть ли резервный фонд - {reserve_fund}, владение частной собственностью - {private_property}, \
    планируемый срок выхода на пассивный доход/пенсию - {retirement} лет, сумма ежемесячной разницы между доходами и расходами - {monthly_income_expenses} рублей, \
    долговые обязательства - {debt_obligation}, возраст инвестора - {age}. Это рискованный, консервативный или умеренный риск-профиль?  Объясни свой выбор."

    return response(prompt, llm, tokenizer)
 

if __name__ == "__main__":
    print(
        risk_profile(
            "рост активов",
            "10 лет",
            "100 тысяч рублей",
            "нет",
            "да",
            "нет",
            "да",
            "нет",
            "да 200 тысяч рублей",
            "да квартира и машина",
            "10 лет",
            "50 тысяч рублей",
            "нет",
            "25 лет",
        )
    )
 