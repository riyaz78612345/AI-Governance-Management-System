from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from database.connection import Base


class AIModel(Base):

    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)

    model_name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    department = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    dataset = Column(String, nullable=False)
    version = Column(String, nullable=False)
    status = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)
    deployment_date = Column(Date, nullable=False)

    risk_assessments = relationship(
        "RiskAssessment",
        back_populates="model",
        cascade="all, delete"
    )

    compliance_assessments = relationship(
        "ComplianceAssessment",
        back_populates="model",
        cascade="all, delete"
    )

    ethics_assessments = relationship(
        "EthicsAssessment",
        back_populates="model",
        cascade="all, delete"
    )


class RiskAssessment(Base):

    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)

    model_id = Column(
        Integer,
        ForeignKey("ai_models.id"),
        nullable=False
    )

    personal_data = Column(Boolean, default=False)
    automated_decision = Column(Boolean, default=False)
    biometric_data = Column(Boolean, default=False)
    human_oversight = Column(Boolean, default=False)
    employment = Column(Boolean, default=False)

    score = Column(Integer, default=0)
    level = Column(String)
    assessment_date = Column(Date)

    model = relationship(
        "AIModel",
        back_populates="risk_assessments"
    )


class ComplianceAssessment(Base):

    __tablename__ = "compliance_assessments"

    id = Column(Integer, primary_key=True, index=True)

    model_id = Column(
        Integer,
        ForeignKey("ai_models.id"),
        nullable=False
    )

    score = Column(Integer, default=0)
    assessment_date = Column(Date)

    model = relationship(
        "AIModel",
        back_populates="compliance_assessments"
    )


class EthicsAssessment(Base):

    __tablename__ = "ethics_assessments"

    id = Column(Integer, primary_key=True, index=True)

    model_id = Column(
        Integer,
        ForeignKey("ai_models.id"),
        nullable=False
    )

    score = Column(Integer, default=0)
    assessment_date = Column(Date)

    model = relationship(
        "AIModel",
        back_populates="ethics_assessments"
    )

class Incident(Base):

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    model_name = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    description = Column(String, nullable=False)

    reported_by = Column(String, nullable=False)

    status = Column(String, nullable=False)

    incident_date = Column(Date, nullable=False)   

class Policy(Base):

    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)

    policy_name = Column(String, nullable=False)

    owner = Column(String, nullable=False)

    category = Column(String, nullable=False)

    effective_date = Column(Date, nullable=False)

    review_date = Column(Date, nullable=False)

    status = Column(String, nullable=False)

class Audit(Base):

    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)

    audit_name = Column(String, nullable=False)

    auditor = Column(String, nullable=False)

    audit_type = Column(String, nullable=False)

    audit_date = Column(Date, nullable=False)

    findings = Column(String, nullable=False)

    status = Column(String, nullable=False)

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)
