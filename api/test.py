from fastapi import FastAPI

app = FastAPI()

# Dosya yolu api/test_api.py olduğu için, Vercel bunu /api/test_api endpoint'ine map edebilir.
# Ya da ana endpoint'i kök (/) yapıp, vercel.json'dan yönlendirebiliriz.
# Şimdilik en basit haliyle kök endpoint yapalım.
@app.get("/")
async def handle_all():
    return {"message": "Test API endpoint from /api/test in api/test.py"}