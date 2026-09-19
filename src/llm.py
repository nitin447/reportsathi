from pathlib import Path

from google import genai
from google.genai import types
from pydantic import BaseModel

from src.config import GEMINI_API_KEY, GEMINI_MODEL

MIME_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


class LLMClient:
    def __init__(self, model: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY missing. Add it to your .env file.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = model

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Plain text answer."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.2,
            ),
        )
        return response.text

    def generate_structured(self, prompt: str, schema: type[BaseModel],
                            system: str | None = None):
        """Answer forced into a Pydantic schema (validated, not free text)."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return response.parsed

    def generate_structured_from_file(self, file_path: str, prompt: str,
                                      schema: type[BaseModel],
                                      system: str | None = None):
        """Read a PDF/image and return structured output."""
        path = Path(file_path)
        mime = MIME_TYPES.get(path.suffix.lower())
        if mime is None:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        part = types.Part.from_bytes(data=path.read_bytes(), mime_type=mime)
        response = self.client.models.generate_content(
            model=self.model,
            contents=[part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return response.parsed