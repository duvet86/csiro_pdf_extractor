from datetime import datetime
from typing import Annotated

from fastapi.params import Depends
from sqlmodel import Column, Field, Relationship, SQLModel, TIMESTAMP, Session, create_engine, text

class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_name: str
    num_pages: int | None = Field(default=None)
    status: str
    extraction_mode: str

    created_datetime: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_datetime: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))

    extracted_data: list["ExtractedData"] = Relationship(back_populates="job")

class ExtractedData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page_number: int
    key: str = Field(index=True)
    value: str

    created_datetime: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_datetime: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))

    job_id: int | None = Field(default=None, foreign_key="job.id")
    job: Job | None = Relationship(back_populates="extracted_data")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
