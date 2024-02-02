from typing import List

from fastapi import FastAPI, HTTPException

from crawler.qualification import get_details, Qualification

app = FastAPI()


@app.post("/qualification")
async def qualification_details(qualifications: List[Qualification]):
    try:
        details = await get_details(qualifications)
        return details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
