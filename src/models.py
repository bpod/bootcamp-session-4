"""
Database models for the Slalom Capabilities Management System.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between capabilities and consultants
capability_consultants = Table(
    'capability_consultants',
    Base.metadata,
    Column('capability_id', Integer, ForeignKey('capabilities.id'), primary_key=True),
    Column('consultant_id', Integer, ForeignKey('consultants.id'), primary_key=True)
)

# Association table for certifications
capability_certifications = Table(
    'capability_certifications',
    Base.metadata,
    Column('capability_id', Integer, ForeignKey('capabilities.id'), primary_key=True),
    Column('certification_id', Integer, ForeignKey('certifications.id'), primary_key=True)
)

# Association table for industry verticals
capability_industries = Table(
    'capability_industries',
    Base.metadata,
    Column('capability_id', Integer, ForeignKey('capabilities.id'), primary_key=True),
    Column('industry_id', Integer, ForeignKey('industries.id'), primary_key=True)
)

# Association table for skill levels
capability_skill_levels = Table(
    'capability_skill_levels',
    Base.metadata,
    Column('capability_id', Integer, ForeignKey('capabilities.id'), primary_key=True),
    Column('skill_level_id', Integer, ForeignKey('skill_levels.id'), primary_key=True)
)


class Capability(Base):
    """Represents a consulting capability in the system."""
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    practice_area = Column(String, nullable=False)
    capacity = Column(Integer, default=0)

    # Relationships
    consultants = relationship(
        "Consultant",
        secondary=capability_consultants,
        back_populates="capabilities"
    )
    certifications = relationship(
        "Certification",
        secondary=capability_certifications,
        back_populates="capabilities"
    )
    industries = relationship(
        "Industry",
        secondary=capability_industries,
        back_populates="capabilities"
    )
    skill_levels = relationship(
        "SkillLevel",
        secondary=capability_skill_levels,
        back_populates="capabilities"
    )


class Consultant(Base):
    """Represents a consultant in the system."""
    __tablename__ = 'consultants'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    capabilities = relationship(
        "Capability",
        secondary=capability_consultants,
        back_populates="consultants"
    )


class Certification(Base):
    """Represents a certification that can be associated with capabilities."""
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    capabilities = relationship(
        "Capability",
        secondary=capability_certifications,
        back_populates="certifications"
    )


class Industry(Base):
    """Represents an industry vertical."""
    __tablename__ = 'industries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    capabilities = relationship(
        "Capability",
        secondary=capability_industries,
        back_populates="industries"
    )


class SkillLevel(Base):
    """Represents a skill level (e.g., Emerging, Proficient, Advanced, Expert)."""
    __tablename__ = 'skill_levels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    capabilities = relationship(
        "Capability",
        secondary=capability_skill_levels,
        back_populates="skill_levels"
    )
