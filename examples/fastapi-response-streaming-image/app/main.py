import boto3
import json
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Story(BaseModel):
    """
    The story class.

    Args:
        BaseModel (_type_): _description_
    """
    topic: Optional[str] = None


@app.post("/")
def api_story(story: Story) -> StreamingResponse:
    """
    API endpoint to get a story.

    Args:
        story (Story): The story object.

    Returns:
        StreamingResponse: The streaming response
    """
    if story.topic is None or story.topic == "":
        return None

    return StreamingResponse(bedrock_stream(story.topic), media_type="text/html")


bedrock = boto3.client('bedrock-runtime')


async def bedrock_stream(topic: str):
    """
    Stream the response from the bedrock model based on the given topic.

    Args:
        topic (str): The topic.
    """
    instruction = f"""
    You are a world class writer. Please write a sweet bedtime story about {topic}.
    """
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": instruction,
            }
        ],
    })

    response = bedrock.invoke_model_with_response_stream(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=body
    )

    stream = response.get('body')
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                message = json.loads(chunk.get("bytes").decode())
                if message['type'] == "content_block_delta":
                    yield message['delta']['text'] or ""
                elif message['type'] == "message_stop":
                    yield "\n"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
