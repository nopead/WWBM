import uvicorn
from fastapi import FastAPI
from src.api.questions import router as questions_router
from src.api.hints import router as hint_router
from src.api.games import router as game_router
from src.api.results import router as result_router
from src.api.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(questions_router)
app.include_router(hint_router)
app.include_router(game_router)
app.include_router(result_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080
    )