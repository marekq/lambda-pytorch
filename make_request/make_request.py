import requests, sys

apigw_url = 'https://x.execute-api.eu-west-1.amazonaws.com/'

inputstr = 'serverless'

def do_inference(path):
    r = requests.post(apigw_url + path, data = inputstr)
    print(path + " - " + r.text)

do_inference('distilbert')
do_inference('bartcnn')
