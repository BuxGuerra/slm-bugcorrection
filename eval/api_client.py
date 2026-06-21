"""Thin wrapper around the official `openai` package, maintaining original interfaces."""
from __future__ import annotations

import os
import time

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency until installed
    openai = None


class APIError(RuntimeError):
    pass


class APIClient:
    def __init__(self, host: str = "http://localhost:8080", request_timeout: int = 120):
        if openai is None:
            raise APIError(
                "The 'openai' package is not installed. Run: pip install openai"
            )
        self.host = host
        
        # OpenAI compatible APIs require the /v1 ending
        base_url = f"{host.rstrip('/')}/v1" if not host.endswith("/v1") else host
        
        # The OpenAI client requires an API key, but in this case, it's not necessary
        api_key = os.environ.get("OPENAI_API_KEY", "dummy-key")
        
        self._client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=request_timeout
        )

    def available_models(self) -> list[str]:
        """Lists the models available locally (or remotely via OpenAI API format)."""
        try:
            response = self._client.models.list()
        except Exception as exc:  # connection refused etc.
            raise APIError(
                f"Could not connect to API at {self.host}. "
                f"Is the server running? Detail: {exc}"
            ) from exc
            
        names = []
        for m in response.data:
            if m.id:
                names.append(m.id)
        return names

    def ensure_model(self, model: str) -> None:
        """Checks that `model` is available"""
        available = self.available_models()

        if model in available or f"{model}:latest" in available:
            return
        raise APIError(
            f"Model '{model}' not found in API. "
            f"The server must be restarted with the correct .gguf file. \nLoaded: {', '.join(available) or '(none)'}"
        )

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
        seed: int | None = None,
        retries: int = 2,
    ) -> str:
        """Generates a response. On error, retries; if it persists, raises APIError."""
        kwargs = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        
        if seed is not None:
            kwargs["seed"] = seed

        last_exc: Exception | None = None
        for attempt in range(retries + 1):
            try:
                resp = self._client.chat.completions.create(**kwargs)
                return resp.choices[0].message.content or ""
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < retries:
                    time.sleep(1.5 * (attempt + 1))
                    
        raise APIError(f"Failed to generate with '{model}': {last_exc}")