from pydantic import BaseModel

class VerificationCode(BaseModel):
    code: str
    password: str