import time
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from aws_lambda_powertools import Logger, Tracer
from codeguru_profiler_agent import with_lambda_profiler

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer()

# load model and tokenizer from local disk
print('start model loading')
startts = time.time()

# load model and tokenizer from local disk
model = AutoModelForSequenceClassification.from_pretrained('./model/', local_files_only = True)
tokenizer = AutoTokenizer.from_pretrained('./model/', local_files_only = True)

endts = time.time()
print('completed model loading in ' + str(round(endts - startts, 2)) + ' seconds')

# lambda handler
@logger.inject_lambda_context(log_event = True)
@tracer.capture_lambda_handler
@with_lambda_profiler()
def handler(event, context):

    # get post string
    message = event['body']
    print(message)

    # analyse sentiment of the submitted text
    rating = pipeline('sentiment-analysis', model = model, tokenizer = tokenizer)(message)

    return {
        'statusCode': 200,
        'body': str(rating)
    }
