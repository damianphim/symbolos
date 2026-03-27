-- Club subscriptions (users subscribing to club events/news)
CREATE TABLE IF NOT EXISTS club_subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    club_id UUID NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    subscribed_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(club_id, user_id)
);

-- Club managers (multiple people can manage a club)
CREATE TABLE IF NOT EXISTS club_managers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    club_id UUID NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    role TEXT DEFAULT 'manager',
    added_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(club_id, user_id)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_club_subscriptions_user ON club_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_club_subscriptions_club ON club_subscriptions(club_id);
CREATE INDEX IF NOT EXISTS idx_club_managers_user ON club_managers(user_id);
CREATE INDEX IF NOT EXISTS idx_club_managers_club ON club_managers(club_id);
