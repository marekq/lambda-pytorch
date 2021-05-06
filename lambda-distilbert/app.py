import base64
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from aws_lambda_powertools import Logger, Tracer

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer()

# load model and tokenizer from local disk
model = AutoModelForSequenceClassification.from_pretrained('./model/', local_files_only = True)
tokenizer = AutoTokenizer.from_pretrained('./model/', local_files_only = True)

# lambda handler
@logger.inject_lambda_context(log_event = True)
@tracer.capture_lambda_handler
def handler(event, context):

    # get post string
    eventstr = event['body']
    print(eventstr)

    # decode from base64
    base64_bytes = eventstr.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # analyse sentiment of the submitted text
    rating = pipeline('sentiment-analysis', model = model, tokenizer = tokenizer)(message)

    return {
        'statusCode': 200,
        'body': str(rating)
    }
