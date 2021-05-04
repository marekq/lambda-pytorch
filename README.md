lambda-pytorch
-------------- 

A simple demo application to serve two ML models of Hugging Face from AWS Lambda. You can deploy the project using AWS CDK and deploys all the infrastructure automatically for you. 

The following models can be invoked through API Gateway using the 'make_request' script:

* t5-large on API path /t5-large
* distilbert-base-uncased-finetuned-sst-2-english on API path /distilbert

The initial "cold" start for both functions can take a few seconds, but "warm" invocations should complete in 1-2 seconds at most. 