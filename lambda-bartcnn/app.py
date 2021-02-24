import base64
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
from aws_lambda_powertools import Logger, Tracer

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer()

# load model and tokenizer from local disk
model = BartForConditionalGeneration.from_pretrained('./model/', local_files_only = True)
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn', local_files_only = False, cache_dir = '/tmp') # fix this to load from local dir instead

# lambda handler
@logger.inject_lambda_context(log_event = True)
@tracer.capture_lambda_handler
def handler(event, context):

    # get post string
    eventstr = event['body']

    # decode from base64
    base64_bytes = eventstr.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # analyse sentiment of the submitted text
    xsum_summarizer = pipeline("summarization", model = model, framework = "pt", tokenizer = tokenizer)
    xsum_result = xsum_summarizer(str(message), min_length = 10, max_length = 100)

    # print and return message
    out = str(message) + " " + str(xsum_result)
    print(out)

    return {
        'statusCode': 200,
        'body': str(out)
    }
