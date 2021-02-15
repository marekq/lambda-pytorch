import base64
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# load model and tokenizer from local disk
model = AutoModelForSequenceClassification.from_pretrained('./model/', local_files_only = True)
tokenizer = AutoTokenizer.from_pretrained('./model/', local_files_only = True)

def handler(event, context):

    # get post string
    eventstr = event['body']

    # decode from base64
    base64_bytes = eventstr.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    # analyse sentiment of the submitted text
    rating = pipeline('sentiment-analysis', model = model, tokenizer = tokenizer)(message)

    # print and return message
    out = str(message) + " " + str(rating)
    print(out)

    return {
        'statusCode': 200,
        'body': str(out)
    }
