from fastapi import FastAPI
from app.users import routers as user_routers
from app.tasks import routers as task_routers
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="askljdhfgjlkasdjfldsanfasdfasdfadsf")
app.include_router(user_routers.auth)
app.include_router(task_routers.tasks)
