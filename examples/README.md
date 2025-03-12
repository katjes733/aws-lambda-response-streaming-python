# Lambda Response Streaming with Python

## Problem statement

AWS Lambda currently only supports node.js for response streaming. Response streaming is useful when large amounts of data are to be transferred from an API to a client. An example would be a case, where an AI model generates a lot of data and a UI is to make this information available to the end-user as it is being generated in real-time. This can improve the user experience significantly as an application is not waiting for the full information to be available but rather displays it as it becomes available.

## Goals

- Support of response streaming when using Python code

## Implementation

There are multiple approaches as to how this can be implemented:

- Docker Image
- Zip file

We will demonstrate both approaches with a simple examples that are functionally identical.

## Build & Deploy

Refer to the specific `README.md` in each example folder.
