from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    TIMESTAMP,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# SQLAlchemy için base sınıfı
Base = declarative_base()

# Veri tabanına bağlantı
engine = create_engine(
    "postgresql+psycopg2://user:password@localhost:5432/database_name"
)


class University(Base):
    __tablename__ = "universities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    icon_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    image_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"))
    cities_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    meta_title = Column(String)
    university_website_url = Column(String)
    ranking_percentile = Column(Numeric)
    ranking_rating = Column(Numeric)
    meta_desc = Column(String)
    meta_img_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
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
    __tablename__ = "programmes"

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
    university_id = Column(UUID(as_uuid=True), ForeignKey("universities.id"))
    discipline_id = Column(UUID(as_uuid=True), ForeignKey("disciplines.id"))
    duration_category_id = Column(
        UUID(as_uuid=True), ForeignKey("duration_categories.id")
    )
    attendance_category_id = Column(
        UUID(as_uuid=True), ForeignKey("attendance_categories.id")
    )
    degree_category_id = Column(UUID(as_uuid=True), ForeignKey("degrees.id"))
    meta_title = Column(String)
    meta_desc = Column(String)
    meta_img_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))
    cities_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"))
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
    university = relationship(
        "University", back_populates="programmes"
    )  # Üniversiteler tablosuna kurulan ilişki tanımlaması
    duration_category_id = Column(
        UUID(as_uuid=True), ForeignKey("duration_categories.id")
    )  # Duration tablosuna olan bağlantı
    duration_category = relationship(
        "DurationCategory", back_populates="programmes"
    )  # Duration tablosu ile ilişki tanımlaması
    discipline_id = Column(
        UUID(as_uuid=True), ForeignKey("disciplines.id")
    )  # Disiplinler tablosu ile olan bağlantı
    discipline = relationship(
        "Discipline", back_populates="programmes"
    )  # Disiplinler tablosu ile kurulan ilişki tanımlaması
    attendance_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attendance_categories.id"),  # Attendance tablosu ile olan bağlantı
    )
    attendance_category = relationship(
        "AttendanceCategory",
        back_populates="programmes",  # Attendance tablosu ile kurulan ilişki
    )

    degree_category_id = Column(
        UUID(as_uuid=True), ForeignKey("degree_categories.id")
    )  # Lisans türlerinin bulunduğu tabloya olan bağlantı

    degree_category = relationship(
        "DegreeCategories", back_populates="programmes"
    )  # Lisans türlerinin bulunduğu tabloya olan ilişki tanımlaması


class Country(Base):
    __tablename__ = "countries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    image_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    icon_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    living_cost = Column(Numeric)
    universities_section_heading = Column(String, default="Popular Universities")
    universities_section_link_label = Column(String, default="View all universities")
    universities_section_link_href = Column(String, default="/universities")
    countries_section_heading = Column(String, default="Discover Your Country")
    countries_section_label = Column(String, default="View all countries")
    countries_section_link_href = Column(String, default="/countries")
    countries_section_heading_dynamic = Column(
        String
    )  # Bunu çekilen veriyle dinamik olarak dolduracağız
    content_section_content = Column(JSON)
    meta_title = Column(String)
    meta_description = Column(String)
    meta_image_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True))

    # İlişkiler
    universities = relationship(
        "University", back_populates="country"
    )  # Üniversiteler ile ilişki
    programmes = relationship(
        "Programme", back_populates="country"
    )  # Programlar ile ilişki
    cities = relationship("City", back_populates="country")  # Şehirler ile ilişki


University.country = relationship("Country", back_populates="universities")
Programme.country = relationship("Country", back_populates="programmes")


class City(Base):
    __tablename__ = "cities"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String, nullable=False)  # Şehir ismi
    slug = Column(String, nullable=False)  # Şehir slug
    image_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))  # Resim bağlantısı
    country_id = Column(
        UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False
    )  # Ülke bağlantısı
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=datetime.utcnow,
        server_default=text("NOW()"),
        nullable=False,
    )

    # İlişkiler
    country = relationship("Country", back_populates="cities")
    image = relationship("Media", foreign_keys=[image_id])


class DurationCategory(Base):
    __tablename__ = "duration_categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String, nullable=False)  # Süre bilgisi (örneğin: 4 sene, 1 sezon)
    slug = Column(String, nullable=False)  # Slug yapısı
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=datetime.utcnow,
        server_default=text("NOW()"),
        nullable=False,
    )

    # İlişki tanımlaması
    programmes = relationship("Programme", back_populates="duration_category")


class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String, nullable=False)  # Disiplinin veya fakültenin ismi
    icon_id = Column(
        UUID(as_uuid=True), ForeignKey("media.id"), nullable=True
    )  # Icon bağlantısı
    slug = Column(String, nullable=False)  # Slug yapısı
    image_id = Column(
        UUID(as_uuid=True), ForeignKey("media.id"), nullable=True
    )  # Resim bağlantısı
    content = Column(JSON, nullable=True)  # Disiplin hakkında bilgi JSON formatında
    extra_content_title = Column(String, nullable=True)  # Ek içerik başlığı
    extra_content_text = Column(String, nullable=True)  # Ek içerik metni
    meta_title = Column(String, nullable=True)  # SEO başlığı
    meta_description = Column(String, nullable=True)  # SEO açıklaması
    meta_image_id = Column(String, nullable=True)  # SEO için resim ID'si
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=datetime.utcnow,
        server_default=text("NOW()"),
        nullable=False,
    )

    # İlişki tanımlaması
    programmes = relationship("Programme", back_populates="discipline")


class AttendanceCategory(Base):
    __tablename__ = "attendance_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())

    # Relationships
    programmes = relationship("Programme", back_populates="attendance_category")


class DegreeCategories(Base):
    __tablename__ = "degree_categories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship to Programmes for degree_category_id
    programmes = relationship("Programmes", back_populates="degree_category")


# Veritabanında tabloları oluştur
Base.metadata.create_all(engine)
