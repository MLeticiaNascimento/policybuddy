from langchain_google_genai import ChatGoogleGenerativeAI

from policybuddy.config import (
    LLM_MODEL,
    GOOGLE_API_KEY,
)


def create_llm():

    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )