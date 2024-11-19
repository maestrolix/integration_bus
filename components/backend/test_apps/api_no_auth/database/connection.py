from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

from database import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)
sessionmaker = _sessionmaker(bind=engine)
