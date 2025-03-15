import json
from nearai.agents.environment import Environment

MODEL = "llama-v3p3-70b-instruct"
VECTOR_STORE_ID = "vs_26f1ed9e727d4ecd8364be1d"


def run(env: Environment):
    user_query = env.list_messages()[-1]["content"]

    # Query the Vector Store
    vector_results = env.query_vector_store(VECTOR_STORE_ID, user_query)
    docs = [{"file": res["chunk_text"]} for res in vector_results[:6]]

    prompt = [
        {
            "role": "user query",
            "content": user_query,
        },
        {
            "role": "documentation",
            "content": json.dumps(docs),
        },
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions about the person’s work according to their emails and slacks data."
        }
    ]

    answer = env.completion(model=MODEL, messages=prompt)
    env.add_reply(answer)


run(env)