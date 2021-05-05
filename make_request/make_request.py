import requests, sys

apigw_url = 'https://x.execute-api.eu-west-1.amazonaws.com/'

if len(sys.argv) > 1:
    ml_input = sys.argv[1]
else:
    ml_input = 'b'

inputstr = '''
AWS Lambda is an event-driven, serverless computing platform provided by Amazon as a part of Amazon Web Services. It is a computing service that runs code in response to events and automatically manages the computing resources required by that code. It was introduced in November 2014.[1]

Node.js, Python, Java, Go,[2] Ruby,[3] and C# (through .NET Core) are all officially supported as of 2018. In late 2018, custom runtime support[4] was added to AWS Lambda.

AWS Lambda supports running native Linux executables via calling out from a supported runtime such as Node.js.[5] For example, Haskell code can be run on Lambda.[6]

AWS Lambda was designed for use cases such as image or object uploads to Amazon S3, updates to DynamoDB tables, responding to website clicks, or reacting to sensor readings from an IoT connected device. AWS Lambda can also be used to automatically provision back-end services triggered by custom HTTP requests, and "spin down" such services when not in use, to save resources. These custom HTTP requests are configured in AWS API Gateway, which can also handle authentication and authorization in conjunction with AWS Cognito.

Unlike Amazon EC2, which is priced by the hour but metered by the second, AWS Lambda is metered by rounding up to the nearest millisecond with no minimum execution time.

In 2019, at AWS' annual cloud computing conference (AWS re:Invent), the AWS Lambda team announced "Provisioned Concurrency", a feature that "keeps functions initialized and hyper-ready to respond in double-digit milliseconds."[7] The Lambda team described Provisioned Concurrency as "ideal for implementing interactive services, such as web and mobile backends, latency-sensitive microservices, or synchronous APIs."[8]
'''

def t5large_inference():

    r = requests.post(apigw_url + 't5large', data = inputstr, timeout = 31)
    print(str(r.elapsed)[5:10] + " sec - t5large\n\n" + ''.join(r.text).strip() + '\n')

def distilbert_inference():

    r = requests.post(apigw_url + 'distilbert', data = inputstr, timeout = 31)
    print(str(r.elapsed)[5:10] + " sec - distilbert\n\n" + ''.join(r.text).strip() + '\n')

def main():

    if ml_input == "d" or ml_input == "distilbert":
        distilbert_inference()

    elif ml_input == "t" or ml_input == "t5large":
        t5large_inference()

    else:
        distilbert_inference()
        t5large_inference()

main()
