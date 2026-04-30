"""Unit + integration tests for the webhook listener."""

import hashlib
import hmac

import pytest
from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.services import listener


SECRET = "jv0dcuio4gk0pwic1dw65gfmpa9oj0ao"
PAYLOAD = '{"eventType":"test","data":{"hello":"world"}}'
TIMESTAMP = "1700000000"


def _expected_signature(payload: str, secret: str, timestamp: str) -> str:
    digest = hmac.new(
        secret.encode("utf-8"),
        f"{timestamp}.{payload}".encode("utf-8"),
        hashlib.sha1,
    ).hexdigest()
    return f"t={timestamp},v1={digest}"


def test_get_payload_signature_format():
    sig = listener.get_payload_signature(PAYLOAD, SECRET, TIMESTAMP)
    assert sig.startswith(f"t={TIMESTAMP},v1=")
    assert sig == _expected_signature(PAYLOAD, SECRET, TIMESTAMP)


def test_validate_signature_matches():
    sig = _expected_signature(PAYLOAD, SECRET, TIMESTAMP)
    assert listener.validate_signature(sig, PAYLOAD, SECRET) is True


def test_validate_signature_mismatch():
    bad = f"t={TIMESTAMP},v1=deadbeef"
    assert listener.validate_signature(bad, PAYLOAD, SECRET) is False


def test_validate_signature_empty_raises():
    with pytest.raises(ValueError):
        listener.validate_signature("", PAYLOAD, SECRET)


def test_listen_event_no_secret():
    msg = listener.listen_event("t=x,v1=y", PAYLOAD, "")
    assert msg == "Success and not validated the secret key as secretkey is empty"


def test_listen_event_matched():
    sig = _expected_signature(PAYLOAD, SECRET, TIMESTAMP)
    msg = listener.listen_event(sig, PAYLOAD, SECRET)
    assert "matched" in msg and "NOT matched" not in msg
    assert SECRET in msg


def test_listen_event_not_matched():
    msg = listener.listen_event(f"t={TIMESTAMP},v1=deadbeef", PAYLOAD, SECRET)
    assert "NOT matched" in msg


def test_root_endpoint():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_listen_event_endpoint_with_secret(monkeypatch):
    monkeypatch.setattr(config.settings, "secret_key", SECRET)
    sig = _expected_signature(PAYLOAD, SECRET, TIMESTAMP)

    client = TestClient(app)
    r = client.post(
        "/api/listenevent",
        content=PAYLOAD,
        headers={"X-SUMT-Signature": sig, "Content-Type": "application/json"},
    )
    assert r.status_code == 200
    assert "matched" in r.text and "NOT matched" not in r.text


def test_listen_event_endpoint_without_secret(monkeypatch):
    monkeypatch.setattr(config.settings, "secret_key", "")

    client = TestClient(app)
    r = client.post(
        "/api/listenevent",
        content=PAYLOAD,
        headers={"X-SUMT-Signature": "t=x,v1=y", "Content-Type": "application/json"},
    )
    assert r.status_code == 200
    assert r.text == "Success and not validated the secret key as secretkey is empty"
