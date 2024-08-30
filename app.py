import uvicorn

# from src.main import app

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8020,
        reload=True,
    )
