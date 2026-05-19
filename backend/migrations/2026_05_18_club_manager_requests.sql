-- ════════════════════════════════════════════════════════════════════
-- Club manager-invite requests
-- Owners/admins now REQUEST other Symbolos users to become admins/managers
-- instead of adding them directly. The recipient sees the request in
-- their Clubs tab and accepts or denies.
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS club_manager_requests (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  club_id         UUID NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
  target_user_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  requested_by    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status          TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'accepted', 'denied', 'cancelled')),
  message         TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  responded_at    TIMESTAMPTZ
);

-- One pending invite per (club, target) at a time; resolved invites can
-- coexist for history.
CREATE UNIQUE INDEX IF NOT EXISTS idx_cmr_pending_unique
  ON club_manager_requests (club_id, target_user_id)
  WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_cmr_target_status
  ON club_manager_requests (target_user_id, status);

CREATE INDEX IF NOT EXISTS idx_cmr_club
  ON club_manager_requests (club_id);
