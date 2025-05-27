from fastapi import FastAPI

app = FastAPI()

@app.get("/api/test")
async def read_root():
    return {"Hello": "World"}