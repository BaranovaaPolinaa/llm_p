from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(
        self,
        message_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ) -> None:
        self._message_repo = message_repo
        self._client = openrouter_client

    async def chat(
        self,
        user_id: int,
        prompt: str,
        system: str | None,
        max_history: int,
        temperature: float,
    ) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})

        history = await self._message_repo.get_last_n(user_id, max_history)
        messages.extend({"role": m.role, "content": m.content} for m in history)
        messages.append({"role": "user", "content": prompt})

        await self._message_repo.add(user_id=user_id, role="user", content=prompt)
        answer = await self._client.chat_completion(messages=messages, temperature=temperature)
        await self._message_repo.add(user_id=user_id, role="assistant", content=answer)

        return answer

    async def get_history(self, user_id: int) -> list[ChatMessage]:
        return await self._message_repo.get_all(user_id)

    async def clear_history(self, user_id: int) -> None:
        await self._message_repo.delete_all_for_user(user_id)
