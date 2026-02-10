from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])