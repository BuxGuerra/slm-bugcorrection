"""Thin wrapper around the official `ollama` package."""
from __future__ import annotations

import time

try:
    import ollama
except ImportError:  # pragma: no cover - optional dependency until installed
    ollama = None


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434", request_timeout: int = 120):
        if ollama is None:
            raise OllamaError(
                "The 'ollama' package is not installed. Run: pip install -r requirements.txt"
            )
        self.host = host
        self._client = ollama.Client(host=host, timeout=request_timeout)

    def available_models(self) -> list[str]:
        """Lists the models available locally in Ollama."""
        try:
            data = self._client.list()
        except Exception as exc:  # connection refused etc.
            raise OllamaError(
                f"Could not connect to Ollama at {self.host}. "
                f"Is the server running (`ollama serve`)? Detail: {exc}"
            ) from exc
        models = data.get("models", [])
        names = []
        for m in models:
            name = m.get("model") or m.get("name")
            if name:
                names.append(name)
        return names

    def ensure_model(self, model: str) -> None:
        """Checks that `model` is available; otherwise suggests pulling it."""
        available = self.available_models()
        # ollama usually normalizes 'foo' -> 'foo:latest'
        if model in available or f"{model}:latest" in available:
            return
        raise OllamaError(
            f"Model '{model}' not found in Ollama. "
            f"Pull it with: ollama pull {model}\nAvailable: {', '.join(available) or '(none)'}"
        )

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
        seed: int | None = None,
        retries: int = 2,
    ) -> str:
        """Generates a response. On error, retries; if it persists, raises OllamaError."""
        options: dict = {"temperature": temperature}
        if seed is not None:
            options["seed"] = seed
        last_exc: Exception | None = None
        for attempt in range(retries + 1):
            try:
                resp = self._client.generate(model=model, prompt=prompt, options=options)
                return resp.get("response", "")
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < retries:
                    time.sleep(1.5 * (attempt + 1))
        raise OllamaError(f"Failed to generate with '{model}': {last_exc}")
