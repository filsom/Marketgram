from fastapi import Request

from marketgram.identity.access.application.get_user import GetUser, GetUserFields
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router
from marketgram.common.port.adapter.container import Container


@router.get('/user/{session_id}')
async def get_user_controller(session_id: str, req: Request):
    async with Container(req) as container:
        query = await container.get(GetUser)

        return await query.execute(
            GetUserFields(session_id)
        )