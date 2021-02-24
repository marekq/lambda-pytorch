lambda-pytorch
-------------- 

A simple demo application to serve two ML models of Hugging Face from AWS Lambda. You can deploy the project using AWS CDK and deploys all the infrastructure automatically for you. 

The following models can be invoked through API Gateway using the 'make_request' script:

* facebook/bart-large-cnn on API path /bartcnn
* distilbert-base-uncased-finetuned-sst-2-english on API path /distilbert

The project is in alpha stage with a lot of work to be done. 
