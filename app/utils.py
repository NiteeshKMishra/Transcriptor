import tiktoken

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def summarization_prompt(text: str):
    return [
        {
            "role": "system",
            "content": f"""
I'll share with you transcript of a recording. Please provide a concise summary of the context in 2-3 sentences,
focusing on key points and important details. You can add information from the internet and other sources
if it adds value to the summary or provided context is not sufficient for summarization.
""".strip(),
        },
        {"role": "user", "content": f"Summarize the following: {text}"},
    ]
