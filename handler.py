import json
import re
import psycopg2
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
SSN_RE = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

def _redact(body: dict):
    redacted = False
    safe = {}
    for k, v in (body or {}).items():
        if isinstance(v, str):
            if EMAIL_RE.search(v):
                safe[k] = '[REDACTED_EMAIL]'
                redacted = True
                continue
            if SSN_RE.search(v):
                safe[k] = '[REDACTED_SSN]'
                redacted = True
                continue
        safe[k] = v
    return safe, redacted

def _pg_smoke():
    dsn = os.environ.get("PG_DSN")
    if not dsn:
        return {"ok": False, "error": "PG_DSN not set"}
    try:
        conn = psycopg2.connect(dsn)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            res = cur.fetchone()
        conn.close()
        return {"ok": True, "result": res[0]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def proxy_handler(event, context):
    headers = (event or {}).get('headers', {}) or {}
    agent_id = headers.get('X-Agent-ID') or headers.get('x-agent-id', 'unknown')
    method = (event or {}).get('httpMethod', 'GET')
    path = (event or {}).get('path', '')

    # Parse JSON body safely
    body_in = {}
    raw = (event or {}).get('body')
    if raw:
        try:
            body_in = json.loads(raw)
        except Exception:
            body_in = {'raw': str(raw)[:100]}

    # Redact PII
    safe_body, redacted = _redact(body_in)

    # Guard example
    if method == 'DELETE' and 'admin' in (path or '').lower():
        return {"statusCode": 403, "body": json.dumps({"error": "Blocked"})}

    resp = {
        "status": "processed",
        "agent_id": agent_id,
        "redacted": redacted,
        "body": safe_body
    }

    # Only add pg field if PG_DSN is configured; never crash request
    if path.endswith('/proxy/test') and os.environ.get("PG_DSN"):
        resp["pg"] = _pg_smoke()

    return {"statusCode": 200, "body": json.dumps(resp)}
