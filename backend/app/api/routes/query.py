import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.middleware import limiter
from app.core.config import get_settings
from app.core.langfuse_client import truncate_text
from app.db.database import get_db
from app.db.models import UsageLog, User
from app.db.repositories import get_documents_by_ids
from app.rag.pipeline import run_pipeline
from app.schemas.query import QueryRequest, QueryResponse, Source, UsageStats

router = APIRouter(tags=["query"])
settings = get_settings()
logger = structlog.get_logger(__name__)


@router.post("/query", response_model=QueryResponse)
@limiter.limit(settings.query_rate_limit)
async def query_documents(
    request: Request,
    payload: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QueryResponse:
    request_id = getattr(request.state, "request_id", None)

    db.add(
        UsageLog(
            user_id=current_user.id,
            endpoint="/query",
            request_id=request_id,
            status_code=status.HTTP_200_OK,
            detail=(
                f"use_hyde={payload.use_hyde},"
                f"use_query_transform={payload.use_query_transform}"
            ),
        )
    )
    db.commit()

    logger.info(
        "query_started",
        question_preview=truncate_text(payload.question, 100),
        use_hyde=payload.use_hyde,
        use_query_transform=payload.use_query_transform,
        max_sources=payload.max_sources,
    )

    try:
        result = await run_pipeline(
            question=payload.question,
            user_id=current_user.id,
            settings=settings,
            use_hyde=payload.use_hyde,
            use_query_transform=payload.use_query_transform,
            max_sources=payload.max_sources,
            trace_id=request_id,
        )
    except Exception as exc:
        logger.exception("query_failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query",
        ) from exc

    document_ids = {source.document_id for source in result.sources}
    documents = get_documents_by_ids(db, current_user.id, list(document_ids))
    filenames = {document.id: document.original_filename for document in documents}

    sources = [
        Source(
            document_id=source.document_id,
            original_filename=filenames.get(
                source.document_id,
                source.original_filename,
            ),
            page_number=source.page_number,
            text=source.text,
            score=source.score,
        )
        for source in result.sources
    ]

    return QueryResponse(
        answer=result.answer,
        sources=sources,
        query_used=result.query_used,
        hyde_used=result.hyde_used,
        query_transform_used=result.query_transform_used,
        usage=UsageStats(
            prompt_tokens=result.usage.prompt_tokens,
            completion_tokens=result.usage.completion_tokens,
            embedding_tokens=result.usage.embedding_tokens,
            total_tokens=result.usage.total_tokens,
            estimated_cost_usd=result.usage.estimated_cost_usd,
        ),
        trace_id=request_id,
    )
