from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import LookupData
from ..schemas import LookupSchema

router = APIRouter()

@router.get("/lookup/getLookupData", response_model=list[LookupSchema])
def get_lookup_data(db: Session = Depends(get_db)):
    return db.query(LookupData).all()
