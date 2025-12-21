# Marketing-Tool

Desktop-style command center for enhancing B2B customer engagement through automation, a creation studio, integrations, analytics, and customer feedback tooling.

## Features

- **Automation dashboard**: manage trigger-based email/pipeline follow-ups per segment.
- **Creation studio**: keep marketing templates (email, decks, social) close at hand.
- **Creative mode**: easy campaign creation for inexperienced users with smart automation.
- **Segmentation**: track key customer groups and their criteria.
- **Connectors & integrations**: quick view of CRM, email, and social connection health plus sync status.
- **Operational health**: backend services and databases with latency, errors, and storage snapshots.
- **Analytics & A/B**: monitor open/click/reply rates and experiment winners.
- **Feedback tools**: surveys/questions you routinely send after demos or onboarding.
- **Morning focus list**: the top few actions to move engagement forward.

## Quick start

1. Create a virtual environment (optional) and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the dashboard summary (uses sample data in `data/state.json` and persists updates):
   ```bash
   python marketing_tool.py --summary
   ```
3. **NEW: Use Creative Mode for easy campaign creation:**
   ```bash
   python marketing_tool.py --creative-mode
   ```
   Creative Mode provides an intuitive interface where you simply describe your campaign idea (e.g., "demo video for SMB CTOs") and the system automatically:
   - Matches your idea to predefined automation rules
   - Configures segments, channels, and cadence
   - Sets up A/B testing variants
   - Provides a split-screen studio for content editing (70%) and automation status (30%)

4. Add a new automation/campaign targeting a segment:
   ```bash
python marketing_tool.py --add-campaign \
  --name "Partner nurture" \
  --segment "Active Customers" \
  --trigger "Quarterly business review" \
  --channel "Email" \
  --template "QBR follow-up" \
  --next-send 2025-01-15  # example date; adjust as needed
```
   Optional: set an initial status with `--status ready|running|paused` (defaults to `scheduled`).
5. Export a snapshot of the dashboard (SVG) to share or pin for your morning routine:
   ```bash
   python marketing_tool.py --snapshot
   ```
   The snapshot is saved to `docs/dashboard_snapshot.svg`.

If you want to restore the original sample data at any time:
```bash
python marketing_tool.py --reset-sample
```

## Creative Mode

Creative Mode is designed for inexperienced users who want to quickly create campaigns without worrying about the technical details. The system includes predefined automation rules that match common scenarios:

- **SMB_CTO**: Campaigns targeting tech leads at small/medium businesses (Email+LinkedIn, 0-3-7 day cadence)
- **Enterprise**: High-touch campaigns for VP-level executives (0-5-14-30 day cadence, 3 A/B test variants)
- **Demo_video**: Video content campaigns (2 variants, 90s length, MP4 vertical format)

Simply describe your idea and let the system handle segments, scheduling, and channel selection automatically!
