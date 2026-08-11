from __future__ import annotations

import getpass


SERVICE = "safe-coding-agent-harness"


def set_api_key(provider: str) -> None:
    try:
        import keyring
    except ImportError as exc:
        raise RuntimeError("install the optional credentials extra: pip install .[credentials]") from exc
    key = getpass.getpass(f"Enter API key for {provider} (hidden): ")
    if not key:
        raise ValueError("API key cannot be empty")
    keyring.set_password(SERVICE, provider, key)


def get_api_key(provider: str) -> str | None:
    try:
        import keyring
    except ImportError:
        return None
    return keyring.get_password(SERVICE, provider)


def clear_api_key(provider: str) -> None:
    try:
        import keyring
    except ImportError as exc:
        raise RuntimeError("install the optional credentials extra: pip install .[credentials]") from exc
    try:
        keyring.delete_password(SERVICE, provider)
    except keyring.errors.PasswordDeleteError:
        pass
