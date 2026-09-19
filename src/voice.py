import base64

from sarvamai import SarvamAI

from src.config import SARVAM_API_KEY
from src.explainer import ExplainedReport

MAX_CHARS = 2400  # Sarvam bulbul:v3 allows 2500 characters per request

LANG_CODES = {"English": "en-IN", "Hindi": "hi-IN", "Bengali": "bn-IN"}

CLOSING = {
    "English": "This explanation is only to help you understand. Please talk to your doctor.",
    "Hindi": "यह जानकारी सिर्फ समझाने के लिए है। कृपया अपने डॉक्टर से बात करें।",
    "Bengali": "এই ব্যাখ্যা শুধু বোঝার জন্য। অনুগ্রহ করে আপনার ডাক্তারের সঙ্গে কথা বলুন।",
}


def build_spoken_script(explained: ExplainedReport, language: str = "English") -> str:
    """Short spoken version: summary, then key points while they fit, then a closing line."""
    e = explained.explanation
    closing = CLOSING.get(language, CLOSING["English"])
    reserve = len(closing) + 1

    script = e.summary.strip()
    if len(script) + reserve > MAX_CHARS:
        script = script[: MAX_CHARS - reserve].rsplit(" ", 1)[0]

    for k in e.key_points:
        line = f"{k.name}. {k.meaning}".strip()
        if len(script) + len(line) + 1 + reserve > MAX_CHARS:
            break
        script += " " + line

    return f"{script} {closing}"


def speak(text: str, language: str = "English", speaker: str = "ritu") -> bytes:
    """Returns WAV audio bytes."""
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY missing. Add it to your .env file.")
    code = LANG_CODES.get(language)
    if code is None:
        raise ValueError(f"Unsupported language: {language}")

    client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
    response = client.text_to_speech.convert(
        text=text,
        language_code=code,
        model="bulbul:v3",
        speaker=speaker,
    )
    return base64.b64decode(response.audios[0])