from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db import Base

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)

    ranges = relationship("SeasonalRange", back_populates="species")

class SeasonalRange(Base):
    __tablename__ = "seasonal_ranges"

    id = Column(Integer, primary_key=True, index=True)
    species_id = Column(Integer, ForeignKey("species.id"))
    season = Column(String)
    source = Column(String)
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))

    species = relationship("Species", back_populates="ranges")
