## README
This module is responsible for ranking the submissions based on the scores provided by the judges. We have employed Claude LLM to resolve any ties based on relevance score generation using abstracts and research labels.
### How to run?
1. Make sure you have databases and data setup from the previous parts.
2. Setup ANTHROPIC_KEY (Anthropic API token) in the env variables as we use LLMs to resolve tiebreakers.
3. Run ranker.py. This will generate ``final_ranking.txt`` which contains the final rankings.