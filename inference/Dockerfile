FROM public.ecr.aws/lambda/python:3.8

# install requirements
COPY requirements.txt ./
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt

# download ML model with wget
RUN yum install wget -y

RUN mkdir model
RUN wget -q https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/config.json -O ./model/config.json
RUN wget -q https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/pytorch_model.bin -O ./model/pytorch_model.bin
RUN wget -q https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/tokenizer_config.json -O ./model/tokenizer_config.json
RUN wget -q https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/vocab.txt -O ./model/vocab.txt

# copy lambda code
COPY app.py ./

# run handler
CMD ["app.handler"]
