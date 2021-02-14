from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# load model and tokenizer from local disk
model = AutoModelForSequenceClassification.from_pretrained('./model/', local_files_only = True)
tokenizer = AutoTokenizer.from_pretrained('./model/', local_files_only = True)

def handler(event, context):

    print(event)
    text = "I like clouds."

    # analyse sentiment of the submitted text
    x = pipeline('sentiment-analysis', model = model, tokenizer = tokenizer)(text)

    print(text, x)

    return str(x)
