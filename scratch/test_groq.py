import os
from langchain_groq import ChatGroq

key = "YOUR_GROQ_KEY_HERE"
model = "llama-3.1-8b-instant"

try:
    llm = ChatGroq(api_key=key, model_name=model)
    res = llm.invoke("Hi")
    print("Success:", res.content)
except Exception as e:
    print("Failed:", str(e))
