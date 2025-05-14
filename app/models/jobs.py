import datetime
import enum

from sqlalchemy import Integer, String, Enum, Float, DATETIME, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base

class BudgetType(enum.Enum):
    FIXED = "fixed_price"
    HOURLY = "hourly_rate"
    NEGOTIABLE = "negotiable"

class LocationType(enum.Enum):
    ONSITE = "on_site"
    REMOTE = "remote"

class JobFiles(Base):
    """
    Model that stores the url of the images used for jobs as well as the specific job associated with each image
    One-to-many relationship with `Jobs`
    """
    __tablename__ = "job_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(255))

class Skills(Base):
    """
    A table for the skills a job might have
    Many-to-many relationship with jobs
    """
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

class JobSkillAssociation(Base):
    """
    Association table to facilitate many-to-many relationship
    between jobs and skills

    (A job can have multiple skills - resilient, hard work, diligent etc -
    and one skill can be required by many jobs - 'Hard work' is needed in many different jobs
    """
    __tablename__ = "job_skill_association"


    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    skill_id: Mapped[str] = mapped_column(String(255), nullable=False)

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description:Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    budget_type: Mapped[BudgetType] = mapped_column(Enum(BudgetType), name="budget_type", nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    expected_delivery_date: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=False)
    location_type: Mapped[LocationType] = mapped_column(Enum(LocationType), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    street_address: Mapped[str] = mapped_column(String(200), nullable=False)

    #foreign key referencing the job creator
    job_creator: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)


class StatusType(enum.Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"


class JobApplications(Base):
    __tablename__ = "job_applications"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    status: Mapped[StatusType] = mapped_column(Enum(StatusType), nullable=False)