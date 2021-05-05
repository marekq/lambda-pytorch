lambda-pytorch
-------------- 

A simple demo application to serve two ML models of Hugging Face from AWS Lambda Docker functions. You can deploy the project using AWS CDK and deploys all the infrastructure automatically for you. Run the 'cdk deploy' command to get started.


Usage
-----

The following models can be invoked through API Gateway using the 'warmerLambda' function:

* t5-large on API path /t5-large
* distilbert-base-uncased-finetuned-sst-2-english on API path /distilbert

The two ML Lambda functions are set with a "Provisioned Concurrency" of 1 to lower the cold start latency impact. This does add a small fixed cost to the stack, but it is the best way to guarantee < 2 second responses. 
