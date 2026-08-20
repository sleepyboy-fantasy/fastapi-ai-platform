from fastapi import FastAPI


app = FastAPI(
    title="FastAPI AI Platform"
)


@app.get("/")
def root():
    return {
        "message": "FastAPI AI Platform running"
    }