import os
from anthropic import Anthropic


def get_prompt(rank_df):
    prompt = f"""
        Given the following dataframe:
        {rank_df}
        Generate a combined relevance score for each record based on similarity between abstract and research labels
        Return a text with 'poster_id', 'average_score', 'final_rank' which resolves the ties and 'relevance_score' fields sorted by relevance and no additional sentences
        Do not truncate the output.
        """
    return prompt


def tie_resolution(rank_df):
    api_key = os.getenv("ANTHROPIC_KEY")
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=100,
        temperature=0,
        messages=[{"role": "user", "content": get_prompt(rank_df)}]
    )
    return response.content[0].text.strip()