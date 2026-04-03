from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 SQLite Database URL
DATABASE_URL = "sqlite:///./company.db"

# 🔥 Create Engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 🔥 Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔥 Base Class
Base = declarative_base()