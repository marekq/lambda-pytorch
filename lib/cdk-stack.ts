import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as Lambda from "@aws-cdk/aws-lambda";
import * as apigateway from "@aws-cdk/aws-apigateway";
import * as events from '@aws-cdk/aws-events';
import * as targets from '@aws-cdk/aws-events-targets';
import { PythonFunction, PythonLayerVersion } from "@aws-cdk/aws-lambda-python";
import { Duration } from "@aws-cdk/core";
import { LambdaIntegration } from "@aws-cdk/aws-apigateway";

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
      timeout: Duration.seconds(30),
      reservedConcurrentExecutions: 3,
      retryAttempts: 0
    });

    /*
    // Add provisioned concurrency of 1
    distilbertLambda.currentVersion.addAlias('live', {
      provisionedConcurrentExecutions: 0
    });
    */

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
      retryAttempts: 0
    });

    /*
    // Add provisioned concurrency of 1
    t5largeLambda.currentVersion.addAlias('live', {
      provisionedConcurrentExecutions: 0
    });
    */

    //////////////////////////////////////

    const api = new apigateway.LambdaRestApi(this, 'myapi', {
      handler: distilbertLambda,
      proxy: false
    });

    api.root.addResource('distilbert').addMethod('POST', new LambdaIntegration(distilbertLambda))
    api.root.addResource('t5large').addMethod('POST', new LambdaIntegration(t5largeLambda))

    //////////////////////////////////////

    const warmerLambda = new PythonFunction(this, "warmerLambda", {
      entry: "./lambda-warmer",
      index: "app.py",
      handler: "lambda_handler",
      runtime: Lambda.Runtime.PYTHON_3_8,
      tracing: Lambda.Tracing.ACTIVE,
      memorySize: 256,
      timeout: Duration.seconds(59),
      retryAttempts: 0,
      environment: {
        'apigw': api.url
      },
      layers: [
        new PythonLayerVersion(this, 'LambdaLayer', {
          entry: path.join(__dirname, '../lambda-layer'),
          compatibleRuntimes: [Lambda.Runtime.PYTHON_3_8],
        }),
      ]
    });  

    // Create EventBridge rule that will execute our Lambda every 2 minutes
    const cronSchedule = new events.Rule(this, 'scheduledLambda', 
      {
        schedule: events.Schedule.expression('rate(1 minute)')
      }
    )
  
    // Set the target of our EventBridge rule to our Lambda function
    cronSchedule.addTarget(new targets.LambdaFunction(warmerLambda));
  }
}