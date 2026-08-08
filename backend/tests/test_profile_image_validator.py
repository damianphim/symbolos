"""
F-06 regression tests for UserUpdate.profile_image.

The validator was widened to accept same-origin proxy URLs
(https://symbolos.ca/storage/profile-images/...) alongside the original
direct Supabase Storage URLs, so avatars can be served from our own origin
where our security headers (nosniff) actually apply.

Widening a security control is the risky kind of change, so these tests pin
down that it is still an ALLOWLIST. F-06 exists to stop profile_image being
pointed at an arbitrary URL — tracking pixel, attacker-hosted SVG, or an
unbounded data: blob stored straight in the row.
"""
import pytest
from pydantic import ValidationError

from api.routes.users import UserUpdate

SUPA = "https://jgkfeyqnpsivbgoiekze.supabase.co"


def _set(url):
    return UserUpdate(profile_image=url).profile_image


class TestAccepted:
    def test_direct_supabase_url_still_works(self):
        """Rows written before the proxy hold this shape — must keep working."""
        u = f"{SUPA}/storage/v1/object/public/profile-images/abc/avatar.png"
        assert _set(u) == u

    def test_same_origin_proxy_url(self):
        u = "https://symbolos.ca/storage/profile-images/abc/avatar.png"
        assert _set(u) == u

    def test_none_and_empty_pass_through(self):
        assert UserUpdate(profile_image=None).profile_image is None
        assert UserUpdate(profile_image="   ").profile_image is None


class TestRejected:
    @pytest.mark.parametrize("url", [
        "https://evil.example.com/storage/profile-images/x.png",   # not our host
        "https://symbolos.ca.evil.com/storage/profile-images/x.png",  # suffix trick
        # Pre-existing F-06 bypass found while writing these tests: the host
        # check used `in` (substring), so an attacker-registered domain ending
        # in the project host passed. Now an exact match.
        f"{SUPA}.evil.com/storage/v1/object/public/profile-images/x.svg",
        "https://notjgkfeyqnpsivbgoiekze.supabase.co/storage/v1/object/public/profile-images/x.png",
        "http://symbolos.ca/storage/profile-images/x.png",         # not https
        "https://symbolos.ca/uploads/x.png",                       # wrong path
        "https://symbolos.ca/storage/club-logos/x.png",            # wrong bucket
        f"{SUPA}/storage/v1/object/public/club-logos/x.png",       # wrong bucket
        "data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=",              # data URI
        "javascript:alert(1)",                                     # scheme abuse
    ])
    def test_hostile_urls_are_rejected(self, url):
        with pytest.raises(ValidationError):
            UserUpdate(profile_image=url)

    def test_arbitrary_https_is_not_blanket_allowed(self):
        """The whole point of F-06 — widening must not have opened this up."""
        with pytest.raises(ValidationError):
            UserUpdate(profile_image="https://tracker.example.com/pixel.png")
