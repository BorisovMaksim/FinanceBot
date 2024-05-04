# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster 

WORKDIR /app

COPY bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install dff[postgresql]
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# cache mfaq model
#RUN ["python3", "-c", "from sentence_transformers import SentenceTransformer; _ = SentenceTransformer('clips/mfaq')"]

COPY . .

CMD ["python3", "bot/run.py"]
