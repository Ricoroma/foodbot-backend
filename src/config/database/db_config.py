from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.project_config import database_path

engine = create_engine(f'sqlite:///{database_path}', isolation_level='AUTOCOMMIT')
engine.connect()
Session = sessionmaker(engine)
Session.configure(bind=engine)
