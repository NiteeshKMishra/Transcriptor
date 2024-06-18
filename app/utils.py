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
I'll share with you transcript of a recording. Please provide summary of the context in 1-2 sentences,
focusing on key points and important details. You can add information from the internet and other sources
if it adds value to the summary or provided context is not sufficient for summarization. Imitate the sentiment
of the transcription in the summary.
""".strip(),
        },
        {"role": "user", "content": f"Summarize the following: {text}"},
    ]

# Few shot prompting
def sentiment_analysis_prompt(text: str):
    return [
        {
            "role": "system",
            "content": """
I will provide you summary of transcription. Tell me if sentiment of the summary is positive or negative:
""".strip(),
        },
        {"role": "user", "content": "The book 'Wuthering Heights' is very boring. This book should not be recommended to anyone."},
        {"role": "assistant", "content": "negative"},
        {"role": "user", "content": "The weather in England in very pleasant. This makes england a popular holiday destination for lot of tourists"},
        {"role": "assistant", "content": "positive"},
        {"role": "user", "content": f"{text}"},
    ]
