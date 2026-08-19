from datetime import datetime, timedelta, timezone

import jwt

from src.domain.entities import Doctor


class JwtTokenIssuer:
    def __init__(self, secret: str, algorithm: str, expires_minutes: int):
        self.secret = secret
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes

    def issue(self, doctor: Doctor) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(doctor.id),
            "username": doctor.username,
            "iat": now,
            "exp": now + timedelta(minutes=self.expires_minutes),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])
