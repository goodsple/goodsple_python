# app/services/rasa_service.py
import os
import httpx
from dataclasses import dataclass

RASA_URL = os.getenv("RASA_PARSE_URL", "http://127.0.0.1:5005/model/parse")

@dataclass
class NluResult:
    intent: str
    confidence: float
    ok: bool
    raw: dict

async def parse_intent(text: str) -> NluResult:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(RASA_URL, json={"text": text})
        r.raise_for_status()
        data = r.json() if "application/json" in r.headers.get("content-type", "") else {}
        intent_obj = data.get("intent") or {}
        intent = intent_obj.get("name")
        conf = float(intent_obj.get("confidence", 0.0) or 0.0)
        return NluResult(intent=intent or "nlu_fallback",
                         confidence=conf,
                         ok=bool(intent),
                         raw=data)
    except Exception:
        # Rasa 미응답/비정상 응답 시 안전 반환
        return NluResult(intent="nlu_fallback", confidence=0.0, ok=False, raw={})