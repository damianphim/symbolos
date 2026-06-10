# Secrets rotation runbook

What to do when a credential leaks, an employee/contributor leaves, or
you're doing routine hygiene. Each secret has: where it lives, how to
rotate it, and what breaks during the swap.

**Golden rule:** rotate in this order — (1) generate new, (2) add new to
Vercel, (3) redeploy, (4) verify, (5) revoke old. Never revoke first or
you take the site down.

---

## Inventory — every secret and where it lives

| Secret | Service | Used by | Stored in |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic | chat, cards, electives, transcript | Vercel (backend) |
| `SUPABASE_SERVICE_KEY` | Supabase | all backend DB writes | Vercel (backend) |
| `SUPABASE_ANON_KEY` | Supabase | frontend client | Vercel (frontend) + in JS bundle |
| `SUPABASE_URL` | Supabase | both | Vercel (both) |
| `RESEND_API_KEY` | Resend | verification + reminder + feedback email | Vercel (backend) + Supabase SMTP |
| `RESEND_WEBHOOK_SECRET` | Resend | bounce webhook verification | Vercel (backend) |
| `ADMIN_SECRET` | self-issued | admin panel auth | Vercel (backend) |
| `CRON_SECRET` | self-issued | daily cron auth | Vercel (backend) |
| `SENTRY_DSN` / `VITE_SENTRY_DSN` | Sentry | error telemetry | Vercel (both) |
| `SENTRY_AUTH_TOKEN` | Sentry | source-map upload at build | Vercel (frontend build) |
| `VITE_POSTHOG_KEY` | PostHog | analytics | Vercel (frontend) |
| `LOGTAIL_TOKEN` | Better Stack | log shipping | Vercel (backend) |
| `HEALTHCHECK_URL` | Healthchecks.io | cron heartbeat | Vercel (backend) |
| `SLACK_WEBHOOK_URL` | Slack | feedback notifications | Vercel (backend) |

---

## Generic rotation procedure

```bash
# 1. Generate a NEW value at the provider's dashboard (don't delete old yet).
# 2. Update it in Vercel:
#    Project → Settings → Environment Variables → edit → Save
# 3. Redeploy so the new value takes effect:
vercel --prod        # or push a commit / click "Redeploy" in the dashboard
# 4. Verify the site still works (sign in, send a chat, etc.).
# 5. NOW revoke/delete the old value at the provider.
```

---

## Per-secret specifics

### ANTHROPIC_API_KEY (leaked → urgent: it costs money)
1. console.anthropic.com → API Keys → Create Key.
2. Update Vercel backend env, redeploy.
3. Test: send a chat message, confirm a response.
4. Delete the old key in the Anthropic console.
5. Check Usage for any spike during the exposure window.

### SUPABASE_SERVICE_KEY (leaked → CRITICAL: full DB access)
This is the master key — full read/write bypassing RLS.
1. Supabase → Project Settings → API → "Reset service_role key" (or
   "Generate new JWT secret" if the whole signing secret leaked — that
   rotates ALL keys including anon).
2. **If you reset the JWT secret**, every existing user session is
   invalidated — they'll have to sign in again. Acceptable in a breach.
3. Update Vercel backend env, redeploy.
4. Test sign-in + a DB write (favorite a course).

### SUPABASE_ANON_KEY (leaked is less severe — it's in the bundle anyway)
The anon key is *designed* to be public; RLS is what protects data. You
only rotate this if you rotated the JWT secret (which rotates both).
Update Vercel frontend env, redeploy, hard-refresh.

### RESEND_API_KEY (leaked → someone can send mail as you)
1. resend.com → API Keys → Create.
2. Update in **two** places: Vercel backend env AND Supabase → Auth →
   SMTP settings (password field).
3. Redeploy backend, save Supabase SMTP.
4. Test: trigger a verification email to yourself.
5. Delete the old key in Resend.
6. Watch dmarcian for any spoofed mail sent during exposure.

### ADMIN_SECRET / CRON_SECRET (self-issued)
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Update Vercel, redeploy. For CRON_SECRET also update the Vercel cron
config if it passes the secret as a header (check vercel.json /
dashboard cron settings). Test by hitting the admin login / manually
triggering the cron.

### SENTRY_AUTH_TOKEN (build-time only)
Lowest risk — it can only upload source maps to your Sentry project.
sentry.io → Settings → Auth Tokens → revoke + create. Update Vercel
frontend build env.

---

## When a contributor leaves

Rotate everything they could have seen: at minimum
`SUPABASE_SERVICE_KEY`, `ANTHROPIC_API_KEY`, `RESEND_API_KEY`,
`ADMIN_SECRET`, `CRON_SECRET`. Remove them from:
- GitHub repo collaborators
- Vercel team
- Supabase organization
- Resend team
- Sentry / PostHog / Better Stack orgs

---

## Routine hygiene

Rotate `ADMIN_SECRET` and `CRON_SECRET` every 6 months (cheap, no user
impact). The provider keys (Anthropic, Supabase, Resend) only on
suspicion of compromise or staff change — rotating them has a small
blast radius each time.
