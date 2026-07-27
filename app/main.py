from fastapi import FastAPI

app = FastAPI(title="Sistema de Reservas de Canchas API")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Reservas de Canchas Backend"}
