import structlog
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.middleware import limiter
from app.core.langfuse_client import get_langfuse
from app.db.database import get_db
from app.db.models import UsageLog, User
from app.schemas.query import FeedbackRequest, FeedbackResponse

router = APIRouter(tags=["feedback"])
logger = structlog.get_logger(__name__)


@router.post("/feedback", response_model=FeedbackResponse)
@limiter.limit("60/hour")
async def submit_feedback(
    request: Request,
    payload: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FeedbackResponse:
    request_id = getattr(request.state, "request_id", None)
    score_value = 1.0 if payload.value == "positive" else 0.0

    langfuse = get_langfuse()
    langfuse.create_score(
        trace_id=payload.trace_id,
        name="user_feedback",
        value=score_value,
        comment=payload.comment,
    )
    langfuse.flush()

    comment_length = len(payload.comment) if payload.comment else 0
    db.add(
        UsageLog(
            user_id=current_user.id,
            endpoint="/feedback",
            request_id=request_id,
            status_code=status.HTTP_200_OK,
            detail=f"feedback={payload.value},trace={payload.trace_id}",
        )
    )
    db.commit()

    logger.info(
        "feedback_recorded",
        trace_id=payload.trace_id,
        feedback_value=payload.value,
        comment_length=comment_length,
    )

    return FeedbackResponse(status="recorded")
