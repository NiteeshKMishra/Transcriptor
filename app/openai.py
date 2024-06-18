from dotenv import dotenv_values
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from app.utils import summarization_prompt, sentiment_analysis_prompt,  num_tokens_from_messages

SECRETS_FILE = "secrets.env"
temperature = 0.7
model = "gpt-3.5-turbo"
max_tokens = 4096
response_tokens = 150

config = dotenv_values(SECRETS_FILE)
client = OpenAI(api_key=config["OPEN_AI_API_KEY"])

@retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIConnectionError)
    | retry_if_exception_type(APIError)
    | retry_if_exception_type(RateLimitError),
)
def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        temperature=temperature,
        response_format="json",
    )

    return transcription.text

@retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIConnectionError)
    | retry_if_exception_type(APIError)
    | retry_if_exception_type(RateLimitError),
)
def translate_audio(file_path):
    audio_file = open(file_path, "rb")
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        temperature=temperature,
        response_format="json",
    )
    return translation.text

@retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIConnectionError)
    | retry_if_exception_type(APIError)
    | retry_if_exception_type(RateLimitError),
)
def summarize_transcription(text: str):
    prompt_tokens = num_tokens_from_messages(summarization_prompt(""))
    offset_tokens = prompt_tokens + response_tokens
    excerpt = text

    # keep removing last 5 words until tokens are under max_tokens
    while num_tokens_from_messages(summarization_prompt(excerpt)) - offset_tokens >= max_tokens:
        words = excerpt.split(" ")
        excerpt = " ".join(words[:-5])

    messages = summarization_prompt(excerpt)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


@retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIConnectionError)
    | retry_if_exception_type(APIError)
    | retry_if_exception_type(RateLimitError),
)
def sentiment_analysis(text: str):
    messages = sentiment_analysis_prompt(text)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content
