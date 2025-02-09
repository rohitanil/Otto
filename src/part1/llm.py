import os
from anthropic import Anthropic


def get_prompt(abstract, judges, top_k):
    prompt = f"""
        Given the following research abstract:
        {abstract}

        Rank the top 5 professors based on their research interests. The list of professors is given below:
        {judges}

        Return a JSON list of dictionaries with 'id', and 'relevance_score' fields sorted by relevance. I just need the json list nothing else. No new line characters,
        weird spacing etc. Do not truncate the output.
        """
    return prompt


def top_k_judges(abstract, judges):
    K = 5
    api_key = os.getenv("ANTHROPIC_KEY")
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=100,
        temperature=0,
        messages=[{"role": "user", "content": get_prompt(abstract, judges, K)}]
    )
    return response.content[0].text.strip()

