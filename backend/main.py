from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello, World! O backend e o frontend estão se comunicando perfeitamente."}
