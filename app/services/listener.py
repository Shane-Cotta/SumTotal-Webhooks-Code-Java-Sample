"""Listener service - validates webhook payload signatures (HMAC-SHA1)."""

import hashlib
import hmac
import logging

log = logging.getLogger("Listener")

HMAC_ALGORITHM = hashlib.sha1


def listen_event(signature: str, payload: str, secret_key: str) -> str:
    """Entry point for processing an inbound webhook event.

    Mirrors the Java `Listener.ListenEvent` behavior: when a secret key is
    configured we regenerate the signature and compare it to the value sent
    in the `X-SUMT-Signature` request header.
    """
    if secret_key:
        signature_valid = validate_signature(signature, payload, secret_key)
        if signature_valid:
            log.info(
                "validated the secretkey with the payload signature and result is matched and secretkey is : %s",
                secret_key,
            )
            return (
                "Success and validated the secretkey with the payload signature "
                f"and result is matched and secretkey is :{secret_key}"
            )
        log.info(
            "validated the secretkey with the payload signature and result is NOT matched and secretkey is : %s",
            secret_key,
        )
        return (
            "Success and validated the secretkey with the payload signature "
            f"and result is NOT matched and secretkey is : {secret_key}"
        )

    log.info("not validated the secret key as secretkey is empty")
    return "Success and not validated the secret key as secretkey is empty"


def validate_signature(signature: str, payload: str, secret_key: str) -> bool:
    """Recompute the signature from the payload and compare to the header value."""
    if not signature or not payload:
        raise ValueError("Exception: Payload/Signature is null or empty.")

    # Header format: "t=<timestamp>,v1=<hex-digest>"
    signature_parts = signature.split(",")
    timestamp = signature_parts[0].split("=")[1]

    signature_from_payload = get_payload_signature(payload, secret_key, timestamp)
    log.info("signatureFromPayload : %s", signature_from_payload)

    return hmac.compare_digest(signature_from_payload, signature)


def get_payload_signature(payload: str, secret_key: str, timestamp: str) -> str:
    """Build the canonical "t=<ts>,v1=<sig>" signature string for a payload."""
    payload_to_sign = f"{timestamp}.{payload}"
    digest = hmac.new(
        secret_key.encode("utf-8"),
        payload_to_sign.encode("utf-8"),
        HMAC_ALGORITHM,
    ).hexdigest()
    return f"t={timestamp},v1={digest}"
