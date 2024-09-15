from fastapi import FastAPI 
from src.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Socail Media App",
    description="A simple social api",
    version="0.1",

)