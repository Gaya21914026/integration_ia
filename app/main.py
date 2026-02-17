from fastapi import FastAPI
from app.routers.products import router as products_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.db.database import Base,engine




app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(chat_router)