from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    model_path: Path | None
    threads: int
    context: int
    max_tokens: int

    @classmethod
    def from_values(
        cls,
        model: str | None = None,
        threads: int | None = None,
        context: int | None = None,
        max_tokens: int | None = None,
    ) -> "AppConfig":
        model_value = model or os.getenv("QL_MODEL_PATH")
        default_model = Path("models/model.gguf")
        model_path = Path(model_value) if model_value else default_model
        if not model_path.exists():
            model_path = None

        return cls(
            model_path=model_path,
            threads=threads or int(os.getenv("QL_THREADS", "4")),
            context=context or int(os.getenv("QL_CONTEXT", "2048")),
            max_tokens=max_tokens or int(os.getenv("QL_MAX_TOKENS", "256")),
        )
