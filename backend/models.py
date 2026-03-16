from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from pydantic import BaseModel
from typing import Optional, List


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    form = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    regulations = relationship("Regulation", back_populates="product")


class Regulation(Base):
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    country = Column(String, nullable=False)
    authority = Column(String, nullable=False)
    hs_code = Column(String, nullable=False)
    hs_description = Column(Text, nullable=False)
    duty_rate = Column(String, nullable=False)
    duty_notes = Column(Text)
    systems_approach = Column(Text)
    regulatory_authorities = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="regulations")
    permits = relationship("Permit", back_populates="regulation")


class Permit(Base):
    __tablename__ = "permits"

    id = Column(Integer, primary_key=True, index=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id"), nullable=False)
    permit_type = Column(String, nullable=False)
    authority = Column(String, nullable=False)
    required = Column(String, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    regulation = relationship("Regulation", back_populates="permits")


class ComplianceNote(Base):
    __tablename__ = "compliance_notes"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentUpload(Base):
    __tablename__ = "document_uploads"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    country = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    uploaded_at = Column(DateTime, default=datetime.utcnow)


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class PermitSchema(BaseModel):
    permit_type: str
    authority: str
    required: str
    notes: Optional[str]

    class Config:
        from_attributes = True


class RegulationSchema(BaseModel):
    country: str
    authority: str
    hs_code: str
    hs_description: str
    duty_rate: str
    duty_notes: Optional[str]
    systems_approach: Optional[str]
    regulatory_authorities: Optional[str]
    permits: List[PermitSchema] = []

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    product_id: str
    name: str
    category: str
    form: str
    country: str
    regulations: List[RegulationSchema] = []

    class Config:
        from_attributes = True


class ComplianceCheckRequest(BaseModel):
    product_id: str
    destination_country: str
    documents_uploaded: List[str] = []


class ComplianceCheckResponse(BaseModel):
    product_id: str
    destination_country: str
    hs_code: str
    duty_rate: str
    required_permits: List[PermitSchema]
    missing_documents: List[str]
    gap_count: int
    status: str


class DocumentUploadSchema(BaseModel):
    product_id: str
    country: str
    document_type: str
    filename: str
    status: Optional[str] = "uploaded"

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    product_id: Optional[str] = None
    country: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []