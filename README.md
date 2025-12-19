# Marketing-Tool

Desktop-style command center for enhancing B2B customer engagement through automation, a creation studio, integrations, analytics, and customer feedback tooling.

## Features

- **Automation dashboard**: manage trigger-based email/pipeline follow-ups per segment.
- **Creation studio**: keep marketing templates (email, decks, social) close at hand.
- **Segmentation**: track key customer groups and their criteria.
- **Integrations**: quick view of CRM, email, and social connection health.
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
3. Add a new automation/campaign targeting a segment:
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
4. Export a snapshot of the dashboard (SVG) to share or pin for your morning routine:
   ```bash
   python marketing_tool.py --snapshot
   ```
   The snapshot is saved to `docs/dashboard_snapshot.svg`.

If you want to restore the original sample data at any time:
```bash
python marketing_tool.py --reset-sample
```
