-- ════════════════════════════════════════════════════════════════════
-- advisor_cards: allow the new "advice" category
-- Run this in the Supabase SQL Editor.
--
-- api/routes/cards.py added CARD_CATEGORIES = [..., "advice"] but the table's
-- advisor_cards_category_check CHECK constraint was never updated, so any
-- generated "advice" card 500s on insert (Sentry: 23514 violates check
-- constraint "advisor_cards_category_check").
--
-- NOTE: "other" is included below even though it's no longer in the app's
-- CARD_CATEGORIES list — it was a legacy category value and existing rows
-- still carry it, so the constraint must keep allowing it or this migration
-- itself fails with the same 23514 error against historical data.
-- ════════════════════════════════════════════════════════════════════

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'advisor_cards_category_check'
  ) THEN
    EXECUTE 'ALTER TABLE advisor_cards DROP CONSTRAINT advisor_cards_category_check';
  END IF;
END $$;

ALTER TABLE advisor_cards
  ADD CONSTRAINT advisor_cards_category_check
  CHECK (category IN ('deadlines', 'degree', 'courses', 'grades', 'planning', 'opportunities', 'advice', 'other'));
