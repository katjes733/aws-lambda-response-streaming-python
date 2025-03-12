# Serverless Bedtime Storyteller using Image

This example shows how to use Lambda Web Adapter to run a `FastAPI` application with response streaming via a Function URL.

## How does it work?

This example uses Anthropic Claude v2 model to generate bedtime stories. `FastAPI` provides the static web frontend and an inference API. The inference API endpoint invokes Bedrock using `Boto3`, and streams the response. Both Lambda Web Adapter and function URL have response streaming mode enabled. So the response from Bedrock are streamed all the way back to the client.

This function is packaged as a Docker image. Because the `aws-lambda-adapter` is only supporting `amd64` architecture, the lambda function architecture can only be `x86_64`.

**NOTE:** The corresponding zip example uses `arm64` architecture, because it utilizes an arm64 lambda layer.

In the SAM template, we use an environment variable `AWS_LWA_INVOKE_MODE: RESPONSE_STREAM` to configure Lambda Web Adapter in response streaming mode. And adding a function url with `InvokeMode: RESPONSE_STREAM`.

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
export AWS_PROFILE=<PROFILE>
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
