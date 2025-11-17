from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import SeasonalRange
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/range/{species_code}")
def get_ranges(species_code: str, db: Session = Depends(get_db)):
    ranges = db.query(SeasonalRange).filter(
        SeasonalRange.species.has(code=species_code)
    ).all()

    if not ranges:
        raise HTTPException(status_code=404, detail="Species not found")

    response = {}

    for r in ranges:
        season = r.season
        geom = to_shape(r.geom)  # convert WKB to Shapely geometry
        geojson = mapping(geom)  # convert to GeoJSON

        if season not in response:
            response[season] = []

        response[season].append({
            "geom": geojson,
            "source": r.source
        })

    return {"species_code": species_code, "ranges": response}
