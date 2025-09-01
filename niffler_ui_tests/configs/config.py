from pydantic import BaseModel


class Service(BaseModel):
    http: str | None = None


class Microservice(BaseModel):
    frontend_niffler: Service | None = None


class Config(BaseModel):
    app: Microservice | None = None
