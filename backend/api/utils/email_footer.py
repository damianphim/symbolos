"""
CASL-compliant email footer (Canada's Anti-Spam Legislation).

CASL § 6 requires every Commercial Electronic Message (CEM) to include:
  1. The sender's identity and a way to contact them (valid for 60 days).
  2. A working unsubscribe mechanism that takes effect within 10 business days.

Strictly transactional messages (account verification, password reset)
are exempt under § 6(6) — but calendar reminders and any future digest /
announcement emails are borderline, and the safe, cheap move is to put a
compliant footer on EVERYTHING. The only thing a transactional email
needs to drop is the word "unsubscribe" implying they can opt out of
security mail — so we phrase it as "manage notification preferences".

Physical mailing address: CASL requires a real postal address. Update
SENDER_POSTAL below with the address you want to disclose (a P.O. box is
fine and keeps your home address private).
"""
from __future__ import annotations

import os

# A physical mailing address is legally required in the footer. A P.O.
# box is acceptable. Override via env so it isn't hard-coded in the repo.
SENDER_POSTAL = os.getenv(
    "SENDER_POSTAL_ADDRESS",
    "Symbolos · Montreal, Quebec, Canada",
)
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "symbolosadvsry@gmail.com")


def casl_footer_html(unsubscribe_url: str = "https://symbolos.ca", *, transactional: bool = False) -> str:
    """Return the HTML footer block to append inside the email's footer cell.

    transactional=True  → security/account mail. Shows "manage preferences"
                          but not a hard unsubscribe (you can't opt out of
                          verification mail and still use the account).
    transactional=False → reminders / digests. Shows a real unsubscribe link.
    """
    if transactional:
        action = (
            f'<a href="{unsubscribe_url}/settings" style="color:#9ca3af;text-decoration:underline;">'
            'Manage notification preferences</a>'
        )
    else:
        action = (
            f'<a href="{unsubscribe_url}/settings?unsubscribe=1" '
            'style="color:#9ca3af;text-decoration:underline;">Unsubscribe</a>'
            ' · '
            f'<a href="{unsubscribe_url}/settings" style="color:#9ca3af;text-decoration:underline;">'
            'Notification settings</a>'
        )

    return (
        f'<span style="display:block;margin-top:6px;color:#9ca3af;font-size:11px;line-height:1.7;">'
        f'{SENDER_POSTAL}<br>'
        f'{action} · '
        f'<a href="mailto:{SUPPORT_EMAIL}" style="color:#9ca3af;text-decoration:underline;">Contact us</a>'
        f'</span>'
    )
