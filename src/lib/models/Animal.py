from pydantic import BaseModel


class Animal(BaseModel):
    name: str
    img_link: str

