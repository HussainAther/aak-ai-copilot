from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from analysis.session_scorer import score_session

router = APIRouter()

# Define input model
class ActivityEvent(BaseModel):
    timestamp: str
    type: str  # e.g., "keyboard", "mouse_click", "mouse_move", "screenshot"
    metadata: Optional[dict] = {}

class SessionData(BaseModel):
    employee_id: str
    task_info: Optional[List[dict]] = []
    events: List[ActivityEvent]

# Route for scoring a session
@router.post("/score_session")
async def score_employee_session(session_data: SessionData):
    try:
        result = score_session(session_data.dict())
        return {"status": "success", "score_report": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

