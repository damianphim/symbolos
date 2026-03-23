-- Newsletter system tables
-- Run this in the Supabase SQL Editor

-- 1. Newsletter Sources — curated list of McGill newsletters
CREATE TABLE IF NOT EXISTS newsletter_sources (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  url         TEXT NOT NULL DEFAULT '',
  feed_type   TEXT DEFAULT 'web',          -- 'rss' | 'ical' | 'web'
  category    TEXT DEFAULT 'general',
  logo_url    TEXT,
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- 2. Newsletter Subscriptions — per-user subscription tracking
CREATE TABLE IF NOT EXISTS newsletter_subscriptions (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  source_id     UUID NOT NULL REFERENCES newsletter_sources(id) ON DELETE CASCADE,
  calendar_sync BOOLEAN DEFAULT true,
  email_muted   BOOLEAN DEFAULT false,
  created_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, source_id)
);

-- 3. Newsletter Events — events parsed from newsletter feeds
CREATE TABLE IF NOT EXISTS newsletter_events (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id     UUID NOT NULL REFERENCES newsletter_sources(id) ON DELETE CASCADE,
  title         TEXT NOT NULL,
  description   TEXT,
  date          DATE NOT NULL,
  time          TEXT,             -- HH:MM 24h
  end_time      TEXT,
  location      TEXT,
  link          TEXT,
  external_id   TEXT,             -- dedup key from feed
  created_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(source_id, external_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_nl_subs_user    ON newsletter_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_nl_subs_source  ON newsletter_subscriptions(source_id);
CREATE INDEX IF NOT EXISTS idx_nl_events_source ON newsletter_events(source_id);
CREATE INDEX IF NOT EXISTS idx_nl_events_date   ON newsletter_events(date);

-- Enable RLS
ALTER TABLE newsletter_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_events ENABLE ROW LEVEL SECURITY;

-- RLS Policies: sources are readable by all authenticated users
CREATE POLICY "newsletter_sources_read" ON newsletter_sources
  FOR SELECT TO authenticated USING (true);

-- RLS Policies: subscriptions — users can only manage their own
CREATE POLICY "newsletter_subs_select" ON newsletter_subscriptions
  FOR SELECT TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "newsletter_subs_insert" ON newsletter_subscriptions
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "newsletter_subs_update" ON newsletter_subscriptions
  FOR UPDATE TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "newsletter_subs_delete" ON newsletter_subscriptions
  FOR DELETE TO authenticated USING (auth.uid() = user_id);

-- RLS Policies: events are readable by all authenticated users
CREATE POLICY "newsletter_events_read" ON newsletter_events
  FOR SELECT TO authenticated USING (true);

-- Allow service role full access (for backend API)
CREATE POLICY "newsletter_sources_service" ON newsletter_sources
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "newsletter_subs_service" ON newsletter_subscriptions
  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "newsletter_events_service" ON newsletter_events
  FOR ALL TO service_role USING (true) WITH CHECK (true);


-- ═══════════════════════════════════════════════════════════════════
-- SEED DATA: McGill Newsletter Sources
-- ═══════════════════════════════════════════════════════════════════

INSERT INTO newsletter_sources (name, url, feed_type, category) VALUES
  -- Official University
  ('McGill Reporter',                    'https://reporter.mcgill.ca/',                                              'web', 'University News'),
  ('McGill News (Alumni)',               'https://mcgillnews.mcgill.ca/',                                            'web', 'University News'),
  ('McGill Channels Events',             'https://www.mcgill.ca/channels/section/all/channel_event',                  'web', 'Campus Events'),
  ('Student Services Events',            'https://www.mcgill.ca/studentservices/events',                              'web', 'Campus Events'),
  ('Campus Life & Engagement',           'https://www.mcgill.ca/cle/events',                                         'web', 'Campus Events'),

  -- Student Government
  ('SSMU Listserv',                      'https://ssmu.ca/listserv/',                                                'web', 'Student Life'),
  ('PGSS Newsletter',                    'https://pgss.mcgill.ca/',                                                  'web', 'Student Life'),

  -- Faculty Newsletters
  ('Faculty of Arts Newsletter',         'https://www.mcgill.ca/arts/about/news-0/newsletters-archive',              'web', 'Faculty'),
  ('Faculty of Engineering (EUS Pipeline)', 'https://mcgilleus.ca/',                                                 'web', 'Faculty'),
  ('Desautels Digest',                   'https://www.mcgill.ca/desautels/about/contact/news',                       'web', 'Faculty'),
  ('Faculty of Science',                 'https://www.mcgill.ca/science/about/news',                                 'web', 'Faculty'),

  -- Department / Research
  ('McGill OSS Weekly Newsletter',       'https://www.mcgill.ca/oss/newsletter',                                     'web', 'Science & Research'),
  ('Global Health Newsletter',           'https://www.mcgill.ca/globalhealth/news-publications/newsletters',          'web', 'Science & Research'),
  ('CIRM Newsletter',                    'https://www.mcgill.ca/centre-montreal/resources/newsletter',                'web', 'Science & Research'),
  ('Microbiology & Immunology (MIMM Bites)', 'https://www.mcgill.ca/microimm/newsletter',                           'web', 'Science & Research'),

  -- Student Publications
  ('The McGill Daily',                   'https://www.mcgilldaily.com/',                                              'web', 'Student Publications'),
  ('The Bull & Bear',                    'https://bullandbearmcgill.com/',                                            'web', 'Student Publications'),
  ('The McGill Tribune',                 'https://www.thetribune.ca/',                                                'web', 'Student Publications'),
  ('McLing (Linguistics)',               'https://mcling.blogs.mcgill.ca/',                                           'web', 'Student Publications')

ON CONFLICT DO NOTHING;
