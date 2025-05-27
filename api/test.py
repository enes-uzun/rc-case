from fastapi import FastAPI

app = FastAPI()

# Vercel'den gelen /api/test isteğini karşılamak için route güncellendi
@app.get("/api/test")
async def handle_api_test():
    return {"message": "Test API endpoint for /api/test, served by api/test.py"}