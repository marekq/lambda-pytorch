import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as Lambda from "@aws-cdk/aws-lambda";
import * as apigatewayv2 from "@aws-cdk/aws-apigatewayv2";
import * as apigatewayv2Integrations from "@aws-cdk/aws-apigatewayv2-integrations";
import { PythonFunction, PythonLayerVersion } from "@aws-cdk/aws-lambda-python";
import { Duration } from "@aws-cdk/core";

export class CDKML extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define lambda-distilbert Docker file
    const distilbertDocker = path.join(__dirname, "../lambda-distilbert");

    // Create Lambda function for lambda-distilbert
    const distilbertLambda = new Lambda.DockerImageFunction(this, "distilbert", {
      code: Lambda.DockerImageCode.fromImageAsset(distilbertDocker),
      tracing: Lambda.Tracing.ACTIVE,
      memorySize: 2048,
      timeout: Duration.seconds(60),
      reservedConcurrentExecutions: 3,
      retryAttempts: 1
    });

    // Add provisioned concurrency of 1
    distilbertLambda.currentVersion.addAlias('live', {
      provisionedConcurrentExecutions: 1
    });

    // Create API integration for lambda-distilbert
    const distilbertIntegration = new apigatewayv2Integrations.LambdaProxyIntegration({
      handler: distilbertLambda
    });

    //////////////////////////////////////

    // Define lambda-t5large Docker file
    const t5largeDocker = path.join(__dirname, "../lambda-t5large");

    // Create Lambda function for lambda-t5large
    const t5largeLambda = new Lambda.DockerImageFunction(this, "t5large", {
      code: Lambda.DockerImageCode.fromImageAsset(t5largeDocker),
      tracing: Lambda.Tracing.ACTIVE,
      memorySize: 10240,
      timeout: Duration.seconds(60),
      reservedConcurrentExecutions: 3,
      retryAttempts: 1
    });

    // Add provisioned concurrency of 1
    t5largeLambda.currentVersion.addAlias('live', {
      provisionedConcurrentExecutions: 1
    });

    // Create API Gateway
    const t5largeIntegration = new apigatewayv2Integrations.LambdaProxyIntegration({
      handler: t5largeLambda
    });

    //////////////////////////////////////

    // Create HTTP API
    const httpApi = new apigatewayv2.HttpApi(this, "InferenceAPI");

    // Create API routes
    httpApi.addRoutes({
      path: "/t5large",
      methods: [apigatewayv2.HttpMethod.POST],
      integration: t5largeIntegration
    });

    httpApi.addRoutes({
      path: "/distilbert",
      methods: [apigatewayv2.HttpMethod.ANY],
      integration: distilbertIntegration
    });

    // Print API Gateway endpoint
    new cdk.CfnOutput(this, 'APIGW', {
      value: httpApi.apiEndpoint
    });

    //////////////////////////////////////

    const warmerLambda = new PythonFunction(this, "warmerLambda", {
      entry: "./lambda-warmer",
      index: "app.py",
      handler: "lambda_handler",
      runtime: Lambda.Runtime.PYTHON_3_8,
      tracing: Lambda.Tracing.ACTIVE,
      memorySize: 256,
      timeout: Duration.seconds(60),
      retryAttempts: 1,
      environment: {
        'apigw': httpApi.apiEndpoint
      },
      layers: [
        new PythonLayerVersion(this, 'LambdaLayer', {
          entry: path.join(__dirname, '../lambda-layer'),
          compatibleRuntimes: [Lambda.Runtime.PYTHON_3_8],
        }),
      ]
    });  
  }
}