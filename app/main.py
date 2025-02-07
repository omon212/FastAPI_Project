from fastapi import FastAPI
from app.users import routers as user_routers
from app.tasks import routers as task_routers
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="askljdhfgjlkasdjfldsanfasdfasdfadsf")
app.include_router(user_routers.auth)
app.include_router(task_routers.tasks)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is an API with Bearer authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi