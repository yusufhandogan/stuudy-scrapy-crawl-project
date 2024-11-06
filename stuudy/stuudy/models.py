from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean, DateTime, ForeignKey, JSON, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# SQLAlchemy için base sınıfı
Base = declarative_base()

# Veri tabanına bağlantı
engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/database_name')

class University(Base):
    __tablename__ = 'universities'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    icon_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    image_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))
    cities_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'))
    meta_title = Column(String)
    university_website_url = Column(String)
    ranking_percentile = Column(Numeric)
    ranking_rating = Column(Numeric)
    meta_desc = Column(String)
    meta_img_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))
    student_number = Column(Integer)
    university_type = Column(String)
    foundation_year = Column(String)
    cost_of_living = Column(Numeric)
    school_budget = Column(Numeric)
    dormitory = Column(Numeric)
    overview = Column(JSON)
    about_uni = Column(JSON)
    campus_number = Column(Numeric)
    academic_staff = Column(Numeric)
    history = Column(JSON)

    # İlişki tanımlaması
    programmes = relationship("Programme", back_populates="university")


class Programme(Base):
    __tablename__ = 'programmes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True)
    tuition_fee = Column(Numeric)
    apply_date = Column(DateTime(timezone=True))
    programme_website_url = Column(String)
    ranking_percentile = Column(Numeric)
    ranking_rating = Column(Numeric)
    about_content = Column(JSON)
    featured = Column(Boolean, default=False)
    university_id = Column(UUID(as_uuid=True), ForeignKey('universities.id'))
    discipline_id = Column(UUID(as_uuid=True), ForeignKey('disciplines.id'))
    duration_category_id = Column(UUID(as_uuid=True), ForeignKey('duration_categories.id'))
    attendance_category_id = Column(UUID(as_uuid=True), ForeignKey('attendance_categories.id'))
    degree_id = Column(UUID(as_uuid=True), ForeignKey('degrees.id'))
    meta_title = Column(String)
    meta_desc = Column(String)
    meta_img_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))
    cities_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'))
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))
    credits = Column(String)
    university_logo = Column(String)
    website_of_program = Column(String)
    overview_content = Column(JSON)
    start_dates = Column(String)
    contact_inf = Column(JSON)
    language_proficiency = Column(String)
    program_structure = Column(JSON)
    academic_req = Column(JSON)

    # İlişki tanımlaması
    university = relationship("University", back_populates="programmes")
    duration_category_id = Column(UUID(as_uuid=True), ForeignKey("duration_categories.id")) # Duration tablosuna olan bağlantı
    duration_category = relationship("DurationCategory", back_populates="programmes") # Duration tablosu ile ilişki tanımlaması
    
class Country(Base):
    __tablename__ = 'countries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    image_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    icon_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    living_cost = Column(Numeric)
    universities_section_heading = Column(String, default="Popular Universities")
    universities_section_link_label = Column(String, default="View all universities")
    universities_section_link_href = Column(String, default="/universities")
    countries_section_heading = Column(String, default="Discover Your Country")
    countries_section_label = Column(String, default="View all countries")
    countries_section_link_href = Column(String, default="/countries")
    countries_section_heading_dynamic = Column(String)  # Bunu çekilen veriyle dinamik olarak dolduracağız
    content_section_content = Column(JSON)
    meta_title = Column(String)
    meta_description = Column(String)
    meta_image_id = Column(UUID(as_uuid=True), ForeignKey('media.id'))
    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    # İlişkiler
    universities = relationship("University", back_populates="country") # Üniversiteler ile ilişki
    programmes = relationship("Programme", back_populates="country") # Programlar ile ilişki
    cities = relationship("City", back_populates="country")  # Şehirler ile ilişki

University.country = relationship("Country", back_populates="universities")
Programme.country = relationship("Country", back_populates="programmes")

class City(Base):
    __tablename__ = 'cities'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False)  # Şehir ismi
    slug = Column(String, nullable=False)  # Şehir slug
    image_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))  # Resim bağlantısı
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False)  # Ülke bağlantısı
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow, server_default=text('NOW()'), nullable=False)

    # İlişkiler
    country = relationship("Country", back_populates="cities")
    image = relationship("Media", foreign_keys=[image_id])

class DurationCategory(Base):
    __tablename__ = 'duration_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False)  # Süre bilgisi (örneğin: 4 sene, 1 sezon)
    slug = Column(String, nullable=False)  # Slug yapısı
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow, server_default=text('NOW()'), nullable=False)

    # İlişki tanımlaması
    programmes = relationship("Programme", back_populates="duration_category")


# Veritabanında tabloları oluştur
Base.metadata.create_all(engine)
