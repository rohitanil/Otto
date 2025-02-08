import openai
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#import ace_tools as tools
#openai.api_key = "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"
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[{"role": "system", "content": "Hello, OpenAI!"}]
# )

# print(response["choices"][0]["message"]["content"])


# def get_embedding(text):
#     """Fetches text embedding using OpenAI's text-embedding-ada-002 model."""
#     response = openai.Embedding.create(
#         input=text,
#         model="text-embedding-ada-002"
#     )
#     return response["data"][0]["embedding"]
#
#
# def compute_similarity(professor_texts, topic_texts):
#     """Computes similarity scores between professors and topics."""
#
#     # Generate embeddings for all professors
#     prof_embeddings = [get_embedding(prof) for prof in professor_texts]
#
#     # Generate embeddings for all topics
#     topic_embeddings = [get_embedding(topic) for topic in topic_texts]
#
#     # Convert to numpy arrays
#     prof_matrix = np.array(prof_embeddings)
#     topic_matrix = np.array(topic_embeddings)
#
#     # Compute cosine similarity
#     similarity_matrix = cosine_similarity(prof_matrix, topic_matrix)
#
#     return similarity_matrix
#
#
# # Example data
# professors = [
#     "Dr. Smith specializes in machine learning, AI, and deep learning.",
#     "Prof. Johnson is interested in natural language processing and linguistics.",
#     "Dr. Brown researches cybersecurity and network security."
# ]
#
# topics = [
#     "This research focuses on improving AI-based medical diagnosis systems.",
#     "The paper discusses advancements in NLP for chatbots and dialogue systems.",
#     "A study on enhancing cybersecurity using blockchain technology."
# ]
#
# # Compute similarity scores
# similarity_scores = compute_similarity(professors, topics)
#
# # Convert to DataFrame for better readability
# df = pd.DataFrame(similarity_scores,
#                   index=[f"Professor {i + 1}" for i in range(len(professors))],
#                   columns=[f"Topic {j + 1}" for j in range(len(topics))])
#
# # Round scores to 4 decimal places
# df = df.round(4)
#
# # # Display the results
# #
# #
# # tools.display_dataframe_to_user(name="Professor-Topic Matching Scores", dataframe=df)
