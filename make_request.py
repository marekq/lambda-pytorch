# Run a POST message against the API Gateway

import requests

apigw_url = '<url>'

def do_inference():
    r = requests.post(apigw_url, data = "pytorch is cool")
    print(r.text)

do_inference()
