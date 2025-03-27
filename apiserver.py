from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database Configuration
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Database Model
class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    num1 = Column(Integer)
    num2 = Column(Integer)
    result = Column(Integer)

# Create Tables
Base.metadata.create_all(bind=engine)

# Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 + num2
    calc = Calculation(operation="add", num1=num1, num2=num2, result=result)
    db.add(calc)
    db.commit()
    return {"result": result}
