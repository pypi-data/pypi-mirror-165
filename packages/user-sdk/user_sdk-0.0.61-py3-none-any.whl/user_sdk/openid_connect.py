from typing import List, Dict, Optional
from http import HTTPStatus
import requests

from cachetools import TTLCache
from jose import jwt, ExpiredSignatureError

_LOCAL_CACHE_MAX_SIZE = 2048
_LOCAL_CACHE_TTL_IN_SECONDS = 60 * 60


class OIDCAuthError(Exception):
    def __init__(self, message: str):
        self.message = message


class InsufficientPermissionError(Exception):
    def __init__(self, message: str):
        self.message = message


class OpenIDConnectAuth:
    def __init__(
        self,
        issuer_url: str,
        audience: str,
        algorithms: Optional[List[str]] = None,
        email_claim_key: Optional[str] = None,
    ):
        self._issuer_url = issuer_url
        self._audience = audience
        self._algorithms = algorithms or ["RS256"]
        self._email_claim_key = email_claim_key
        self._cache = TTLCache(
            maxsize=_LOCAL_CACHE_MAX_SIZE, ttl=_LOCAL_CACHE_TTL_IN_SECONDS,
        )

    def authorize(self, access_token: str, required_permission: str = None) -> str:
        try:
            self.validate_access_token(access_token)
        except ExpiredSignatureError:
            raise OIDCAuthError("Access token signature is expired")

        if required_permission and not self._has_permission(
            access_token, required_permission
        ):
            raise InsufficientPermissionError("Insufficient user permission")
        return self._get_user_email(access_token)

    def validate_access_token(self, access_token: str):
        unverified_header = jwt.get_unverified_header(access_token)
        jw_key_set = self._get_jw_key_set()
        rsa_key = self._find_rsa_key(unverified_header["kid"], jw_key_set["keys"])
        jwt.decode(
            access_token,
            rsa_key,
            algorithms=self._algorithms,
            audience=self._audience,
            issuer=self._issuer_url + "/",
        )

    def _get_user_email(self, access_token: str) -> str:
        claims = jwt.get_unverified_claims(access_token)
        if self._email_claim_key and claims.get(self._email_claim_key):
            return claims[self._email_claim_key]

        response = requests.get(
            f"{self._issuer_url}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code != HTTPStatus.OK:
            raise OIDCAuthError("Invalid access token")
        data = response.json()
        if "email" not in data:
            raise OIDCAuthError("Attribute `email` doesn't exist in userinfo.")
        return data["email"]

    def _get_jw_key_set(self) -> Dict:
        cache_key = f"issuer_url:{self._issuer_url}"
        if self._cache.get(cache_key):
            return self._cache.get(cache_key)

        result = requests.get(f"{self._issuer_url}/.well-known/jwks.json").json()
        self._cache.setdefault(cache_key, result)
        return result

    @staticmethod
    def _find_rsa_key(key_id: str, all_keys: List[Dict]) -> Dict:
        for key in all_keys:
            if key["kid"] == key_id:
                return {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

    @staticmethod
    def _has_permission(access_token: str, required_permission: str) -> bool:
        unverified_claims = jwt.get_unverified_claims(access_token)
        permissions = unverified_claims.get("permissions", [])
        if required_permission in permissions:
            return True
        wildcard_permissions = [p for p in permissions if p.endswith("*")]
        for permission in wildcard_permissions:
            if required_permission.startswith(permission.strip("*")):
                return True
        return False


def extract_access_token(authorization_header: str) -> str:
    """Extract Bearer access token from `Authorization` header."""
    if not authorization_header:
        raise OIDCAuthError("Authorization header is expected")
    try:
        bearer, token = authorization_header.split()
    except ValueError:
        raise OIDCAuthError("Invalid bearer token format in authorization header")
    if bearer.lower() != "bearer":
        raise OIDCAuthError("Invalid bearer token format in authorization header")

    return token
