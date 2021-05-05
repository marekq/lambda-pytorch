import requests, os
from aws_lambda_powertools import Logger, Tracer

# initialize powertools logger and tracer
logger = Logger()
tracer = Tracer(patch_modules = [ "requests" ])

inputstr = 'This is a sample text'

@tracer.capture_method(capture_response = False)
def do_inference(path, apigw_url):

    r = requests.post(apigw_url + "/" + path , data = inputstr, timeout = 31)
    print(str(r.elapsed)[5:10] + " sec \t " + path + "\t " + ''.join(r.text).strip() + '\n')

# lambda handler
@logger.inject_lambda_context(log_event = True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    
    apigw_url = os.environ['apigw']
    do_inference('distilbert', apigw_url)
    do_inference('t5large', apigw_url)
