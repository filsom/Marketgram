from dataclasses import dataclass
from typing import Any
from aiohttp import ClientSession
from firebase_admin.auth import verify_id_token, generate_email_verification_link

from marketgram.identity.access.port.adapter.errors import (
    INVALID_CREDENTIALS,
    AuthProviderError
)
from firebase_admin import firestore_async

app = firestore_async.client()


@dataclass(frozen=True)
class FirebaseResponse:
    user_id: str
    email: str


class FirebaseAuthProvider:
    def __init__(
        self, 
        web_api_key: str, 
        session: ClientSession, 
    ) -> None:
        self._web_api_key = {'key': web_api_key}
        self._session = session

    async def sign_up(self, body: dict[str, str]) -> dict[str, str]:
        async with self._session.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signUp',
            params=self._web_api_key,
            data=body
        ) as response:
            if response.status != 200:
                raise AuthProviderError()
            
        async with self._session.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode',
            params=self._web_api_key,
            data={'requestType': 'VERIFY_EMAIL', 'idToken': response['idToken']}
        ) as response:
            if response.status != 200:
                raise AuthProviderError()
        
            try:
                payload = verify_id_token(response['idToken'])
            except Exception:
                raise AuthProviderError()
            
            return {'user_id': payload['user_id'], 'email': payload['email']}

    async def log_in(self, body: dict[str, str]) -> dict[str, str]:
        async with self._session.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
            params=self._web_api_key,
            data=body
        ) as response:
            if response.status != 200:
                raise AuthProviderError()
            
            if not response['email_verified']:
                raise AuthProviderError()
        
            try:
                payload = verify_id_token(response['idToken'])
            except Exception:
                raise AuthProviderError()
            
            return {'user_id': payload['user_id'], 'email': payload['email']}

    async def change_password(self, body: dict[str, str]) -> dict[str, str]:
        async with self._session.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:update',
            params=self._web_api_key,
            data=body
        ) as response:
            if response.status != 200:
                raise AuthProviderError()