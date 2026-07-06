from __future__ import annotations

from functools import lru_cache
from typing import Any, Protocol

from app.core.config import Settings, get_settings


def truncate_text(text: str, max_length: int = 200) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}..."


def normalize_langfuse_trace_id(trace_id: str) -> str:
    """Langfuse expects a 32-char lowercase hex string (UUID without dashes)."""
    return trace_id.replace("-", "").lower()


class ObservationHandle(Protocol):
    def update(self, **kwargs: Any) -> None: ...

    def end(self) -> None: ...


class NullObservation:
    def update(self, **kwargs: Any) -> None:
        return None

    def end(self, **kwargs: Any) -> None:
        return None


class LangfuseObservation:
    def __init__(self, observation: Any | None) -> None:
        self._observation = observation

    def update(self, **kwargs: Any) -> None:
        if self._observation is None:
            return
        self._observation.update(**kwargs)

    def end(self, **kwargs: Any) -> None:
        if self._observation is None:
            return
        if kwargs:
            self._observation.update(**kwargs)
        self._observation.end()


class RagTrace:
    def __init__(
        self,
        client: LangfuseClientProtocol,
        *,
        trace_id: str,
        user_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.trace_id = trace_id
        self._client = client
        self._root = client.start_root_observation(
            trace_id=trace_id,
            name="rag_query",
            metadata=metadata,
        )
        client.set_trace_user(trace_id=trace_id, user_id=user_id, observation=self._root)

    def span(self, name: str, *, input_data: Any | None = None) -> LangfuseObservation:
        observation = self._client.start_child_observation(
            trace_id=self.trace_id,
            parent=self._root,
            name=name,
            as_type="span",
            input_data=input_data,
        )
        return LangfuseObservation(observation)

    def generation(
        self,
        name: str,
        *,
        input_data: Any | None = None,
        model: str | None = None,
    ) -> LangfuseObservation:
        observation = self._client.start_child_observation(
            trace_id=self.trace_id,
            parent=self._root,
            name=name,
            as_type="generation",
            input_data=input_data,
            model=model,
        )
        return LangfuseObservation(observation)

    def finish(self, *, output: Any | None = None) -> None:
        if self._root is not None:
            LangfuseObservation(self._root).end(output=output)


class NullRagTrace:
    trace_id: str

    def __init__(self, trace_id: str) -> None:
        self.trace_id = trace_id

    def span(self, name: str, *, input_data: Any | None = None) -> LangfuseObservation:
        return LangfuseObservation(None)

    def generation(
        self,
        name: str,
        *,
        input_data: Any | None = None,
        model: str | None = None,
    ) -> LangfuseObservation:
        return LangfuseObservation(None)

    def finish(self, *, output: Any | None = None) -> None:
        return None


class LangfuseClientProtocol(Protocol):
    def start_root_observation(
        self,
        *,
        trace_id: str,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Any | None: ...

    def start_child_observation(
        self,
        *,
        trace_id: str,
        parent: Any | None,
        name: str,
        as_type: str,
        input_data: Any | None = None,
        model: str | None = None,
    ) -> Any | None: ...

    def set_trace_user(
        self,
        *,
        trace_id: str,
        user_id: str,
        observation: Any | None,
    ) -> None: ...

    def create_score(
        self,
        *,
        trace_id: str,
        name: str,
        value: float,
        comment: str | None = None,
    ) -> None: ...

    def flush(self) -> None: ...


class NullLangfuse:
    def start_root_observation(
        self,
        *,
        trace_id: str,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        return None

    def start_child_observation(
        self,
        *,
        trace_id: str,
        parent: Any | None,
        name: str,
        as_type: str,
        input_data: Any | None = None,
        model: str | None = None,
    ) -> None:
        return None

    def set_trace_user(
        self,
        *,
        trace_id: str,
        user_id: str,
        observation: Any | None,
    ) -> None:
        return None

    def create_score(
        self,
        *,
        trace_id: str,
        name: str,
        value: float,
        comment: str | None = None,
    ) -> None:
        return None

    def flush(self) -> None:
        return None


class LangfuseWrapper:
    def __init__(self, settings: Settings) -> None:
        from langfuse import Langfuse

        self._client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )

    def _trace_context(self, trace_id: str, parent: Any | None = None) -> dict[str, str]:
        context: dict[str, str] = {"trace_id": trace_id}
        if parent is not None and getattr(parent, "id", None):
            context["parent_span_id"] = parent.id
        return context

    def start_root_observation(
        self,
        *,
        trace_id: str,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        trace_id = normalize_langfuse_trace_id(trace_id)
        return self._client.start_observation(
            trace_context={"trace_id": trace_id},
            name=name,
            as_type="span",
            metadata=metadata,
        )

    def start_child_observation(
        self,
        *,
        trace_id: str,
        parent: Any | None,
        name: str,
        as_type: str,
        input_data: Any | None = None,
        model: str | None = None,
    ) -> Any:
        trace_id = normalize_langfuse_trace_id(trace_id)
        kwargs: dict[str, Any] = {
            "trace_context": self._trace_context(trace_id, parent),
            "name": name,
            "as_type": as_type,
        }
        if input_data is not None:
            kwargs["input"] = input_data
        if model is not None:
            kwargs["model"] = model
        return self._client.start_observation(**kwargs)

    def set_trace_user(
        self,
        *,
        trace_id: str,
        user_id: str,
        observation: Any | None,
    ) -> None:
        if observation is None:
            return
        # langfuse>=4 (OTEL-based SDK) exposes trace-level attributes only via
        # `propagate_attributes()` (a context manager) or by setting the raw OTEL
        # attribute directly. Our observations are created outside of that context
        # manager's lifetime, so we set the underlying span attribute instead.
        otel_span = getattr(observation, "_otel_span", None)
        if otel_span is not None:
            otel_span.set_attribute("user.id", user_id)

    def create_score(
        self,
        *,
        trace_id: str,
        name: str,
        value: float,
        comment: str | None = None,
    ) -> None:
        self._client.create_score(
            trace_id=normalize_langfuse_trace_id(trace_id),
            name=name,
            value=value,
            data_type="NUMERIC",
            comment=comment,
        )

    def flush(self) -> None:
        self._client.flush()


def create_rag_trace(
    client: LangfuseClientProtocol,
    *,
    trace_id: str,
    user_id: int,
    metadata: dict[str, Any] | None = None,
) -> RagTrace | NullRagTrace:
    normalized_trace_id = normalize_langfuse_trace_id(trace_id)
    if isinstance(client, NullLangfuse):
        return NullRagTrace(normalized_trace_id)
    return RagTrace(
        client,
        trace_id=normalized_trace_id,
        user_id=str(user_id),
        metadata=metadata,
    )


@lru_cache
def get_langfuse() -> LangfuseClientProtocol:
    settings = get_settings()
    if not settings.langfuse_enabled:
        return NullLangfuse()
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        return NullLangfuse()
    return LangfuseWrapper(settings)
