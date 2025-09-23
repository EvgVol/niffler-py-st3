from pydantic import BaseModel


class Database(BaseModel):
    host: str
    port: int
    db_name: str
    db_type: str | None = None


class Service(BaseModel):
    http: str | None = None
    database: Database | None = None


class Microservice(BaseModel):
    frontend_niffler: Service | None = None
    auth_niffler: Service | None = None
    currency_niffler: Service | None = None
    spend_niffler: Service | None = None
    userdata_niffler: Service | None = None


class Config(BaseModel):
    app: Microservice | None = None
