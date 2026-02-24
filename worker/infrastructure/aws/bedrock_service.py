import json
import boto3


class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            endpoint_url="http://localstack:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )

    def generate_monthly_insight(self, model_id: str, prompt: str) -> str:
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [])

        if not content:
            raise ValueError("Bedrock returned an empty response")

        return content[0].get("text", "")
