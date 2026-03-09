from fastapi import FastAPI

app = FastAPI(title="API Raízes do Nordeste")

@app.get("/")
def home():
    return {"message": "API funcionando"}