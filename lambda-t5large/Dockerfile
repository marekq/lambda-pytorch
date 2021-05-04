FROM public.ecr.aws/lambda/python:3.8

# download ML model with wget
RUN yum install wget wheel -y

RUN mkdir model
RUN wget -q https://huggingface.co/t5-base/resolve/main/config.json -O ./model/config.json
RUN wget -q https://huggingface.co/t5-base/resolve/main/pytorch_model.bin -O ./model/pytorch_model.bin
RUN wget -q https://huggingface.co/t5-base/resolve/main/tokenizer.json -O ./model/tokenizer.json
RUN wget -q https://huggingface.co/t5-base/resolve/main/spiece.model -O ./model/spiece.model

# install requirements
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip
COPY requirements.txt ./
RUN /var/lang/bin/python3.8 -m pip install --no-cache-dir -r requirements.txt

# copy lambda code
COPY app.py ./

# run handler
CMD ["app.handler"]
