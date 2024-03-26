import json
import google.generativeai as genai

DEFAULT_GEN_CONFIG = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

DEFAULT_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

async def call_gemini(prompt="", generation_config=None, safety_settings=None):
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=DEFAULT_GEN_CONFIG if generation_config is None else generation_config,
                                  safety_settings=DEFAULT_SAFETY_SETTINGS if safety_settings is None else safety_settings)
    response = await model.generate_content_async([prompt])
    return response.text