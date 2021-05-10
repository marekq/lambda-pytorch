lambda-pytorch
-------------- 

A simple demo application to serve two ML models of Hugging Face from AWS Lambda Docker functions. You can deploy the project using AWS CDK and deploys all the infrastructure automatically for you. Run the 'cdk deploy' command to get started.


Usage
-----

The following models can be invoked through API Gateway using the 'warmerLambda' function:

* t5-large on API path /t5-large
* distilbert-base-uncased-finetuned-sst-2-english on API path /distilbert

You can also invoke the Lambda functions directly, setting the inference input in the 'body' field. The same approach can be used with other AWS event sources too. 


Provisioning
------------

There are two ways that you can provision the Lambda functions;

* Default - configured with no Provisioned Concurrency and a Lambda "warmer" function. As a result, you will experience a "cold start" of 5-15 seconds on the initial invocation of the Lambda, but subsequent invocations should take 0.1 - 3 seconds. This mode works best for asynchronous invocations, i.e. through SQS or EventBridge. 
* Configured with a Provisioned Concurrency setting for the ML Lambda's. This does add a static, fixed cost of keeping the functions "warm", but does dramatically reduce the cold start effect for more predictable invokes. This is recommended for synchronous invokes using API Gateway. In order to activate this, uncomment the "provisionedConcurrentExecutions" sections in the CDK stack.  
