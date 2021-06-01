FROM public.ecr.aws/lambda/python:3.8

# download ML model with wget
RUN yum upgrade -y
RUN yum install wget wheel -y

RUN mkdir model
RUN wget -q https://huggingface.co/t5-large/resolve/main/config.json -O ./model/config.json
RUN wget -q https://huggingface.co/t5-large/resolve/main/pytorch_model.bin -O ./model/pytorch_model.bin
RUN wget -q https://huggingface.co/t5-large/resolve/main/tokenizer.json -O ./model/tokenizer.json
RUN wget -q https://huggingface.co/t5-large/resolve/main/spiece.model -O ./model/spiece.model

# install lambda insights logs agent
RUN curl -O https://lambda-insights-extension.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension.rpm && \
    rpm -U lambda-insights-extension.rpm && \
    rm -f lambda-insights-extension.rpm

# install requirements
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip
COPY requirements.txt ./
RUN /var/lang/bin/python3.8 -m pip install --no-cache-dir -r requirements.txt

# copy lambda code
COPY app.py ./

# run handler
CMD ["app.handler"]
