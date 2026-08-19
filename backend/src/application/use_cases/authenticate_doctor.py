from dataclasses import dataclass

from src.domain.entities import Doctor
from src.domain.exceptions import InvalidCredentialsError
from src.domain.ports import DoctorRepository, PasswordHasher, TokenIssuer


@dataclass
class AuthenticateDoctor:
    doctors: DoctorRepository
    hasher: PasswordHasher
    tokens: TokenIssuer

    def execute(self, username: str, password: str) -> str:
        doctor: Doctor | None = self.doctors.get_by_username(username)
        if doctor is None or not self.hasher.verify(password, doctor.password_hash):
            raise InvalidCredentialsError()
        return self.tokens.issue(doctor)
