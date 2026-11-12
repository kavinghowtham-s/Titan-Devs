from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings

# Primary Read-Write Engine
connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

# Read-Only Engine for Safe Text-to-SQL execution (E3)
# Uses SQLite URI mode=ro to ensure OS/engine level write blocking
read_only_db_uri = settings.DATABASE_URL
if "sqlite" in read_only_db_uri:
    # Ensure uri=true is present for SQLAlchemy SQLite URI parameter support
    db_path = read_only_db_uri.replace("sqlite:///", "")
    ro_uri = f"sqlite:///file:{db_path}?mode=ro&uri=true"
    read_only_engine = create_engine(ro_uri, connect_args={"check_same_thread": False})
else:
    read_only_engine = engine

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    if settings.SQLITE_WAL_MODE:
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ReadOnlySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=read_only_engine)

Base = declarative_base()

def get_db():
    """FastAPI Dependency for transactional read-write sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_read_only_db():
    """FastAPI Dependency for strictly sandboxed read-only sessions."""
    db = ReadOnlySessionLocal()
    try:
        yield db
    finally:
        db.close()
