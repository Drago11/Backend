from pydantic import BaseModel


class EmailBody(BaseModel):
    subject: str
    title: str
    body: str
