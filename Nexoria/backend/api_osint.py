from fastapi import APIRouter
from pydantic import BaseModel
from domain_osint import analyze_entity
from security import rate_limit

router = APIRouter()

class OsintRequest(BaseModel):
    tg_id: int
    entity: str

@router.post("/analyze")
def analyze(req: OsintRequest):
    rate_limit(str(req.tg_id))

    result = analyze_entity(req.entity)

    return {
        "summary": f"Тип: {result['type']}\nДанные: {result}",
        "raw": result
    }
