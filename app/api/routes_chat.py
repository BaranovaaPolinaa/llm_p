from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> ChatResponse:
    try:
        answer = await usecase.chat(
            user_id=user_id,
            prompt=payload.prompt,
            system=payload.system,
            max_history=payload.max_history,
            temperature=payload.temperature,
        )
    except ExternalServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=exc.message) from exc
    return ChatResponse(answer=answer)


@router.get("/history", response_model=list[ChatMessageOut], summary="History")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> list[ChatMessageOut]:
    messages = await usecase.get_history(user_id)
    return [ChatMessageOut.model_validate(m) for m in messages]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT, summary="Clear History")
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> None:
    await usecase.clear_history(user_id)
