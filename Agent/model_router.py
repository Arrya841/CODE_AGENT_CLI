from google.genai import errors, types

try:
    from httpx2 import TimeoutException, TransportError
except ImportError:
    from httpx import TimeoutException, TransportError

MODEL_PRIORITY = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

FALLBACK_CODES = {404, 408, 429, 500, 502, 503, 504}
GENERATION_CONFIG = types.GenerateContentConfig(
    automatic_continuation=False,
    http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)),
)


def discover_models(client):
    """Find approved models supporting text generation."""
    available = set()
    for model in client.models.list():
        if "generateContent" in (model.supported_actions or []):
            available.add(model.name.removeprefix("models/"))
    return [model for model in MODEL_PRIORITY if model in available]


def generate_with_fallback(client, contents):
    """Try eligible models until one returns text."""
    print("[Model Router] Discovering available Gemini models", flush=True)
    try:
        candidates = discover_models(client)
    except (TimeoutException, TimeoutError):
        raise RuntimeError("Gemini model discovery timed out.") from None
    except (TransportError, OSError):
        raise RuntimeError("Could not connect to Gemini for model discovery.") from None
    except errors.APIError as error:
        raise RuntimeError(f"Gemini model discovery failed (HTTP {error.code}).") from None

    if not candidates:
        raise RuntimeError("No approved text-generation models were found.")

    failures = []
    for model_name in candidates:
        print(f"[Model Router] Trying {model_name}", flush=True)
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=GENERATION_CONFIG,
            )
            answer = response.text
            if answer and answer.strip():
                print(f"[Model Router] Selected {model_name}", flush=True)
                return answer
            reason = "empty response"
        except (TimeoutException, TimeoutError):
            reason = "request timed out"
        except (TransportError, OSError):
            reason = "network request failed"
        except errors.APIError as error:
            reason = f"HTTP {error.code}"
            if error.code not in FALLBACK_CODES:
                raise RuntimeError(f"Gemini rejected the request ({reason}).") from None

        failures.append(f"{model_name}: {reason}")
        print(f"[Model Router] {model_name} failed ({reason}).", flush=True)

    raise RuntimeError("All eligible models failed: " + "; ".join(failures))
