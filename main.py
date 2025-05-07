import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        port=8002,
        reload=True
    )