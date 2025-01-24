from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./shopApp.db"  
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:vicciSQL@localhost:5432/shop_database"  

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine=create_engine("postgresql://postgres:vicciSQL@localhost:5432/shop_database")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
