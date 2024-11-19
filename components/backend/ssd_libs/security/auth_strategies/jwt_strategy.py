from datetime import datetime, timedelta
from secrets import token_hex

from attr import dataclass
from jose import JWTError, jwt


@dataclass
class JWT:
    _secret_key: str = token_hex(256)
    _access_token_expires_minutes: int = 30
    _algorithm: str = 'HS256'

    def set_secret_key(self, secret_key: str) -> None:
        self._secret_key = secret_key

    def set_access_token_expires_minutes(self, minutes: int) -> None:
        self._access_token_expires_minutes = minutes

    def create_access_token(self, data: dict | None = {}, access_minutes: int | None = None) -> str:
        utc_now = datetime.utcnow()
        if access_minutes is None:
            expire = utc_now + timedelta(minutes=self._access_token_expires_minutes)
        else:
            expire = utc_now + timedelta(minutes=access_minutes)

        to_encode = data.copy()
        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, self._secret_key, self._algorithm)

    def verify_token(self, token: str) -> str:
        try:
            return jwt.decode(token, self._secret_key, self._algorithm)
        except JWTError:
            return None
