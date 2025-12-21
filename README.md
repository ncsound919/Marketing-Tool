# Marketing-Tool

Desktop-style command center for enhancing B2B customer engagement through automation, a creation studio, integrations, analytics, and customer feedback tooling.

## Features

- **Automation dashboard**: manage trigger-based email/pipeline follow-ups per segment.
- **Creation studio**: keep marketing templates (email, decks, social) close at hand.
- **Marketing strategies**: apply proven frameworks (ABM, AIDA, RACE, 7Ps) to customer segments.
- **Video generation**: create marketing videos from templates using MoviePy.
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

## Marketing Strategies

Apply marketing strategies to automatically generate campaigns for your segments:

```bash
# Apply Account-Based Marketing (ABM) strategy to New Leads
python marketing_tool.py --select-strategy ABM --segment "New Leads"

# Apply AIDA (Attention-Interest-Desire-Action) strategy
python marketing_tool.py --select-strategy AIDA --segment "Active Customers"

# Apply RACE (Reach-Act-Convert-Engage) strategy
python marketing_tool.py --select-strategy RACE --segment "Dormant Accounts"

# Apply 7Ps Marketing Mix strategy
python marketing_tool.py --select-strategy 7Ps --segment "Active Customers"
```

Available strategies:
- **ABM** (Account-Based Marketing): Target high-value accounts with personalized campaigns
- **AIDA** (Attention-Interest-Desire-Action): Classic content funnel framework
- **RACE** (Reach-Act-Convert-Engage): Omnichannel planning framework
- **7Ps** (7Ps Marketing Mix): Holistic B2B planning framework

## Video Generation

Generate marketing videos from templates:

```bash
# Generate a video from the "Product Tour Deck" template
python marketing_tool.py --generate-video \
  --template "Product Tour Deck" \
  --output "data/videos/product_tour.mp4"
```

**Note**: Video generation requires `moviepy`. If not installed, you'll see an error message with installation instructions.
