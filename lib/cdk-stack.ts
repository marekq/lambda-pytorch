import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as Lambda from "@aws-cdk/aws-lambda";
import * as apigatewayv2 from "@aws-cdk/aws-apigatewayv2";
import * as apigatewayv2Integrations from "@aws-cdk/aws-apigatewayv2-integrations";
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
      memorySize: 1792,
      timeout: Duration.seconds(60)
    });

    // Create API integration for lambda-distilbert
    const distilbertIntegration = new apigatewayv2Integrations.LambdaProxyIntegration({
      handler: distilbertLambda,
    });

    //////////////////////////////////////

    // Define lambda-bartcnn Docker file
    const bartcnnDocker = path.join(__dirname, "../lambda-bartcnn");

    // Create Lambda function for lambda-bartcnn
    const bartcnnLambda = new Lambda.DockerImageFunction(this, "bartcnn", {
      code: Lambda.DockerImageCode.fromImageAsset(bartcnnDocker),
      tracing: Lambda.Tracing.ACTIVE,
      memorySize: 3008,
      timeout: Duration.seconds(60)
    });

    // Create API Gateway
    const bartcnnIntegration = new apigatewayv2Integrations.LambdaProxyIntegration({
      handler: bartcnnLambda,
    });

    // Create API routes
    const httpApi = new apigatewayv2.HttpApi(this, "InferenceAPI");

    httpApi.addRoutes({
      path: "/bartcnn",
      methods: [apigatewayv2.HttpMethod.ANY],
      integration: bartcnnIntegration
    });

    httpApi.addRoutes({
      path: "/distilbert",
      methods: [apigatewayv2.HttpMethod.ANY],
      integration: distilbertIntegration
    });
  }
}