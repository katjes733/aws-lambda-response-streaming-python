# Serverless Bedtime Storyteller using ZIP

This example shows how to use Lambda Web Adapter to run a `FastAPI` application with response streaming via a Function URL.

## How does it work?

This example uses Anthropic Claude v2 model to generate bedtime stories. `FastAPI` provides the static web frontend and an inference API. The inference API endpoint invokes Bedrock using `Boto3`, and streams the response. Both Lambda Web Adapter and function URL have response streaming mode enabled. So the response from Bedrock are streamed all the way back to the client.

This function is packages as a ZIP file.
Additionally, we add the `aws-lambda-adapter` layer to the function and configure wrapper script.

By default, we use `arm64` for our function architecture using the following layer:

- `arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerArm64:24`

Alternatively, if we wish to use `x86_64` as out function architecture, we would have to use the folowing layer:

- `arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerArm64:24`

Additional configurations are:

1. Configure Lambda environment variable `AWS_LAMBDA_EXEC_WRAPPER` to `/opt/bootstrap`. This is a wrapper script included in the layer.
2. Set function handler to a startup command: `run.sh`. The wrapper script will execute this command to boot up your application.
3. Configure Lambda environment variable `AWS_LWA_INVOKE_MODE: RESPONSE_STREAM` to configure Lambda Web Adapter in response streaming mode. And adding a function url with `InvokeMode: RESPONSE_STREAM`.

## Build and deploy

Run the following commends to build and deploy this example:

```bash
sam build --use-container
sam deploy --guided
```

**NOTE 1:** If you are using AWS SSO, then make sure you have a valid session and use then following command replacing `<PROFILE>` with your SSO session profile:

```bash
sam deploy --guided --profile <PROFILE>
```

Alternatively, you can set the following in your terminal:

```bash
export AWS_PROFILE=PROFILE>
```

**NOTE 2:** When running `sam deploy --guided`, it is highly recommended opting for saving the settings, as subsequent deployment will be simplified by just running `sam deploy`. Remember to always build before to apply any changes:

```bash
sam build --use-container
sam deploy
```

**NOTE 3:** When running `sam deploy --guided`, it will ask you if it is OK to have the lambda deploy without authorization. Confirm this with `y`, but be aware that this the Lambda URL will be public and can theoretically be invoked by anyone. Use caution!

## Test the example

After the deployment completes, copy the `FastAPIFunctionUrl` shown in the output messages.

Execute the following command:

```bash
curl -X POST <FastAPIFunctionUrl> -d '{"topic": "SNS and SQS"}' -H "Content-Type: application/json" --no-buffer
```

This will stream the response directly in your terminal

## Cleanup

To remove all created resources, simply run the following command:

```bash
sam delete
```

**NOTE:** For security reasons (the Function URL is public with no authentication), you should perform a cleanup as soon as you have concluded your work.
