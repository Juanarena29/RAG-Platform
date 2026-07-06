from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    max_sources: int = Field(default=5, ge=1, le=20)
    use_hyde: bool = True
    use_query_transform: bool = True


class Source(BaseModel):
    document_id: int
    original_filename: str
    page_number: int
    text: str
    score: float


class UsageStats(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    embedding_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    query_used: str
    hyde_used: bool
    query_transform_used: bool
    usage: UsageStats
    trace_id: str | None = None


class FeedbackRequest(BaseModel):
    trace_id: str
    value: Literal["positive", "negative"]
    comment: str | None = Field(default=None, max_length=500)


class FeedbackResponse(BaseModel):
    status: str
