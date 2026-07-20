"""
Tests for Settings' production-only required env vars.

Without INNGEST_SIGNING_KEY/INNGEST_EVENT_KEY set in production, every
Inngest callback to /api/inngest fails signature validation and every
transcript/syllabus background job silently fails — this used to only
surface as a "missing signing key" error deep in Sentry. Settings should
now fail fast at startup instead.
"""
from __future__ import annotations

import pytest

from api.config import Settings


def _base_kwargs(**overrides):
    kwargs = {
        "SUPABASE_URL": "https://fake.supabase.co",
        "SUPABASE_SERVICE_KEY": "fake-service-key",
        "ANTHROPIC_API_KEY": "sk-ant-fake0000000000000000000000000000000000000000",
        "CRON_SECRET": "a" * 32,
        "ADMIN_SECRET": "a" * 32,
        "ADMIN_EMAILS": "admin@mail.mcgill.ca",
    }
    kwargs.update(overrides)
    return kwargs


def test_production_requires_inngest_signing_key():
    with pytest.raises(ValueError, match="INNGEST_SIGNING_KEY must be set in production"):
        Settings(**_base_kwargs(ENVIRONMENT="production", INNGEST_SIGNING_KEY="", INNGEST_EVENT_KEY="signkey"))


def test_production_requires_inngest_event_key():
    with pytest.raises(ValueError, match="INNGEST_EVENT_KEY must be set in production"):
        Settings(**_base_kwargs(ENVIRONMENT="production", INNGEST_SIGNING_KEY="signkey", INNGEST_EVENT_KEY=""))


def test_production_passes_with_both_inngest_keys_set():
    settings = Settings(**_base_kwargs(
        ENVIRONMENT="production", INNGEST_SIGNING_KEY="signkey", INNGEST_EVENT_KEY="eventkey",
    ))
    assert settings.INNGEST_SIGNING_KEY == "signkey"
    assert settings.INNGEST_EVENT_KEY == "eventkey"


def test_development_does_not_require_inngest_keys():
    settings = Settings(**_base_kwargs(ENVIRONMENT="development"))
    assert settings.INNGEST_SIGNING_KEY == ""
    assert settings.INNGEST_EVENT_KEY == ""
