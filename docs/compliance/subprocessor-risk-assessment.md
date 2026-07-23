# Subprocessor risk assessment

This is the written record behind the sentence in the Privacy Policy (§4,
`privacy.s4Intro`): *"before relying on them we assessed this cross-border
processing as Law 25 requires."* Quebec's Law 25 (s. 17) requires that
before personal information is communicated outside Quebec, the sensitivity
of the information, the purpose of use, the protections it would receive in
the destination jurisdiction, and that jurisdiction's legal framework are
assessed. This document is that assessment, one entry per subprocessor,
kept current with the list actually disclosed in the Privacy Policy.

**Maintained by:** the Privacy Officer named in Privacy Policy §10.
**Review trigger:** any time a subprocessor is added, dropped, or its data
handling changes — not on a fixed calendar. Last reviewed: 2026-07-23.

**Scope note:** this is the developer's own documented risk judgment, not a
legal opinion or a substitute for signed data-processing agreements. None
of the subprocessors below have a bilaterally negotiated DPA in place today
— each is relied on under its own standard public privacy policy / terms of
service. That's flagged per-vendor below as the residual gap it is; signing
DPAs is tracked as a pre-partnership item, not done here.

---

## Anthropic (Claude API)

- **Data shared:** chat messages, syllabus/transcript text (after local PII
  redaction — see Privacy Policy §2b), course context assembled for AI
  features. Never: name, email, username, McGill student ID, permanent code.
- **Purpose:** the AI advisor, cards, transcript parsing, elective
  recommendations — the product's core feature; no lower-data-footprint way
  to do this exists.
- **Region:** United States. **Cross-border: yes.**
- **Sensitivity:** moderate — academic content and free-text chat, but
  identifiers are stripped before the call (see `_scrub_pii` and transcript
  redaction in `transcript.py`).
- **Destination-jurisdiction protections relied on:** Anthropic's published
  API data-handling terms (API inputs/outputs not used for model training
  by default; no human review absent abuse investigation).
- **Gap:** no signed DPA. Relying on Anthropic's standard terms only.
- **Conclusion:** acceptable given PII stripping is enforced before the call
  reaches this subprocessor at all, minimizing what a US legal-process
  request against Anthropic could ever expose.

## Vercel

- **Data shared:** HTTP request metadata (IP, path, headers) via hosting
  and serverless function execution logs.
- **Purpose:** hosting the frontend and backend — no alternative avoids this.
- **Region:** United States. **Cross-border: yes.**
- **Sensitivity:** low — infrastructure/access logs, not academic content.
- **Retention:** logs ~30 days (per Privacy Policy §4).
- **Gap:** no signed DPA.
- **Conclusion:** acceptable — standard hosting-log exposure, short retention.

## Supabase

- **Data shared:** the full application database — accounts, courses,
  transcripts, chat history, forum content. The single largest data
  footprint of any subprocessor.
- **Purpose:** database and authentication — foundational, no alternative.
- **Region:** disclosed today as "Canada/US" in the Privacy Policy — **this
  is a known gap, not a completed assessment.** Law 25 s. 17 requires
  assessing the *actual* destination jurisdiction; "Canada/US" as an
  either/or means that assessment hasn't really been done yet. Action
  item: confirm the exact region the Supabase project is provisioned in
  and tighten both this document and the Privacy Policy to match.
- **Sensitivity:** high — this is the primary store of personal and
  academic data.
- **Gap:** no signed DPA; region not pinned down (see above).
- **Conclusion:** provisionally acceptable (Supabase's stated security
  practices — encryption in transit and at rest, RLS enforced on our side),
  but the region ambiguity should be resolved before this is a real Law 25
  assessment rather than a placeholder for one.

## Resend

- **Data shared:** recipient email address, verification/reminder email
  content (no academic data — transactional email only).
- **Purpose:** account verification and calendar reminder emails.
- **Region:** not currently pinned down in the Privacy Policy — treat as a
  gap alongside Supabase's.
- **Sensitivity:** low — email address plus templated notification content.
- **Gap:** no signed DPA; region not documented.
- **Conclusion:** acceptable given the low sensitivity, but region should be
  documented for the same reason as Supabase.

## Sentry

- **Data shared:** error/crash telemetry — explicitly *not* message bodies,
  per Privacy Policy §4 ("user IDs only").
- **Purpose:** operational error monitoring.
- **Sensitivity:** low — a user ID is an identifier but not sensitive
  content by itself.
- **Gap:** no signed DPA; region not documented.
- **Conclusion:** acceptable — minimal, non-content data.

## PostHog

- **Data shared:** anonymous product-analytics events; respects
  Do-Not-Track and can be disabled client-side.
- **Purpose:** understanding feature usage.
- **Sensitivity:** low — anonymous by design.
- **Gap:** no signed DPA.
- **Conclusion:** acceptable.

## dmarcian

- **Data shared:** aggregate email-authentication (SPF/DKIM/DMARC) reports
  only — never message content, per Privacy Policy §4.
- **Purpose:** detecting email spoofing / deliverability issues.
- **Sensitivity:** very low — aggregate domain-level stats, not tied to
  individual users.
- **Gap:** no signed DPA.
- **Conclusion:** acceptable.

---

## Open action items

1. Pin down the actual hosting region for Supabase and Resend; stop
   describing Supabase as "Canada/US" once confirmed.
2. Revisit this document if any subprocessor is added, replaced, or a
   region changes — that's also the trigger to update Privacy Policy §4.
3. Signed DPAs with each vendor remain out of scope until there's an actual
   institutional partner asking for them (see the compliance gap list this
   document originated from).
