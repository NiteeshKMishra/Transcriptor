from dotenv import dotenv_values
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

SECRETS_FILE = "secrets.env"
temperature = 0.7

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
def translate_audio(audio_file):
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        temperature=temperature,
        response_format="json",
    )
    return translation.text
