import base64
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from aws_lambda_powertools import Logger, Tracer

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer()

# load model and tokenizer from local disk
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-xsum", cache_dir = "./model/", local_files_only = True)
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-xsum", cache_dir = "./model/", local_files_only = True)

# lambda handler
@logger.inject_lambda_context(log_event = True)
@tracer.capture_lambda_handler
def handler(event, context):

    # get post string
    eventstr = event['body']
    print('body ' + eventstr)

    # decode from base64
    base64_bytes = eventstr.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # analyse sentiment of the submitted text
    xsum_summarizer = pipeline('summarization', model = model, tokenizer = tokenizer)
    xsum_result = xsum_summarizer(message, min_length = 5, max_length = 100)

    # print and return message
    out = str(message) + " " + str(xsum_result)
    print(out)

    return {
        'statusCode': 200,
        'body': str(out)
    }
