from google.genai import errors

MODEL_PRIORITY = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

FALLBACK_CODES = {404, 429, 500, 502, 503, 504}

def discover_models(client):
    """Find approved models supporting text generation.""" 
    avaiable = set()
    for model in client.models.list():
        actions = model.supported_actions or []
        if "generateContent" in actions:
            avaiable.add(model.name.removeprefix("models/"))
    return [
        model for model in MODEL_PRIORITY
        if model in avaiable
    ]

def generate_with_fallback(client, prompt):
    """Try eligible models until one succeeds."""
    candidates = discover_models(client)

    # print("[DEBUG] Eligible models:", candidates)
    # print("[DEBUG] Number of candidates:", len(candidates))

    if not candidates:
        raise RuntimeError(
            "No approved text-generation models were found."
        )
    failures =[]
    
    for model_name in candidates:
        print(f"[Model Router] Trying {model_name}")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if not response.text:
                failures.append(
                    f"{model_name}: Empty response"
                )
                continue

            print(f"[Model Router] Selected {model_name}")
            return response.text

        except errors.APIError as error:
            if error.code not in FALLBACK_CODES:
                raise

            failures.append(
                f"{model_name}: HTTP {error.code}"
            )

            print(
                f"[Model Router] {model_name} failed "
                f"({error.code}). Trying fallback."
            )
    raise RuntimeError(
        "All eligible models failed:\n"
        + "\n".join(failures)
    )
  