import base64, json, sentencepiece, time, torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from aws_lambda_powertools import Logger, Tracer

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer()

# load model and tokenizer from local disk
print('start model loading')
startts = time.time()

model = T5ForConditionalGeneration.from_pretrained('./model/', local_files_only = True)
tokenizer = T5Tokenizer.from_pretrained('./model/', local_files_only = True)
device = torch.device('cpu')

endts = time.time()
print('completed model loading in ' + str(round(endts - startts, 2)) + ' seconds')

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

    # summarize the text
    preprocess_text = message.strip().replace("\n","")
    t5_prepared_text = "summarize: " + preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors = "pt").to(device)
    summary_ids = model.generate(
        tokenized_text,
        num_beams = 4,
        no_repeat_ngram_size = 1,
        min_length = 10,
        max_length = 100,
        length_penalty = 0.8,
        early_stopping = True
    )
    output = tokenizer.decode(summary_ids[0], skip_special_tokens = True)
    print(output)

    # print and return message
    return {
        'statusCode': 200,
        'body': str(output)
    }
