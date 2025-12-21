#!/usr/bin/env python3
"""A lightweight desktop-style dashboard for B2B customer engagement."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "state.json"
DEFAULT_SNAPSHOT_PATH = BASE_DIR / "docs" / "dashboard_snapshot.svg"
COLOR_BG_PRIMARY = "#0b1220"
COLOR_BG_SECONDARY = "#11192d"
COLOR_ACCENT_CYAN = "#38bdf8"
COLOR_ACCENT_PURPLE = "#a78bfa"
COLOR_ACCENT_GREEN = "#22c55e"
COLOR_ACCENT_AMBER = "#f59e0b"
DATETIME_HEADER_FMT = "%b %d, %Y %H:%M"
BACKGROUND_STYLE = f"on {COLOR_BG_PRIMARY}"
DIM_BACKGROUND_STYLE = f"on {COLOR_BG_SECONDARY}"
GLASS_ROW_STYLES = [BACKGROUND_STYLE, DIM_BACKGROUND_STYLE]


DASHBOARD_THEME = Theme(
    {
        "muted": "#cbd5e1",
        "info": "#93c5fd",
        "success": COLOR_ACCENT_GREEN,
        "warning": "#eab308",
        "danger": "#ef4444",
    }
)
STYLE_MUTED = "muted"  # matches the "muted" key defined in DASHBOARD_THEME


def themed_console(*, record: bool = False) -> Console:
    return Console(record=record, theme=DASHBOARD_THEME, style=STYLE_MUTED, color_system="truecolor")


def _today_iso() -> str:
    return datetime.now().date().isoformat()


def sample_state() -> Dict[str, Any]:
    tomorrow = datetime.now().date() + timedelta(days=1)
    return {
        "profile": {"business_name": "Acme Components", "owner": "You"},
        "segments": [
            {
                "name": "New Leads",
                "criteria": ["Created < 30 days", "Matches ICP industries"],
                "size": 34,
            },
            {
                "name": "Active Customers",
                "criteria": ["Touched product in last 14 days"],
                "size": 18,
            },
            {
                "name": "Dormant Accounts",
                "criteria": ["No activity > 30 days"],
                "size": 12,
            },
        ],
        "campaigns": [
            {
                "name": "Onboarding Drip",
                "segment": "New Leads",
                "trigger": "Sign-up form",
                "channel": "Email",
                "template": "Welcome Series",
                "status": "scheduled",
                "next_send": tomorrow.isoformat(),
            },
            {
                "name": "Win-back Sequence",
                "segment": "Dormant Accounts",
                "trigger": "Inactivity 30d",
                "channel": "Email",
                "template": "Re-engagement",
                "status": "ready",
                "next_send": tomorrow.isoformat(),
            },
            {
                "name": "Post-demo Follow-up",
                "segment": "Active Customers",
                "trigger": "Demo completed",
                "channel": "Email + Call task",
                "template": "Demo Recap",
                "status": "running",
                "next_send": _today_iso(),
            },
        ],
        "templates": [
            {
                "name": "Welcome Series",
                "medium": "Email",
                "purpose": "Onboarding",
                "last_updated": _today_iso(),
            },
            {
                "name": "Re-engagement",
                "medium": "Email",
                "purpose": "Win-back",
                "last_updated": _today_iso(),
            },
            {
                "name": "Product Tour Deck",
                "medium": "Presentation",
                "purpose": "Sales enablement",
                "last_updated": _today_iso(),
            },
        ],
        "integrations": [
            {"name": "CRM (HubSpot)", "status": "connected", "detail": "API token valid"},
            {"name": "Email (SendGrid)", "status": "connected", "detail": "Sender verified"},
            {"name": "Social (LinkedIn)", "status": "pending", "detail": "OAuth to finish"},
        ],
        "connectors": [
            {
                "name": "HubSpot contacts",
                "status": "connected",
                "last_sync": _today_iso(),
                "detail": "Contacts + deals",
            },
            {
                "name": "LinkedIn Ads",
                "status": "pending",
                "last_sync": "—",
                "detail": "Finish OAuth to pull audiences",
            },
            {
                "name": "SendGrid events",
                "status": "connected",
                "last_sync": _today_iso(),
                "detail": "Bounces + clicks ingested",
            },
        ],
        "backend": [
            {
                "service": "Engagement API",
                "status": "healthy",
                "latency_ms": 180,
                "error_rate": "0.2%",
                "version": "v1.4.2",
            },
            {
                "service": "Automation Worker",
                "status": "degraded",
                "latency_ms": 420,
                "error_rate": "1.1%",
                "version": "v1.3.9",
            },
        ],
        "databases": [
            {
                "name": "Postgres",
                "role": "Primary",
                "status": "healthy",
                "storage_gb": 12.4,
                "connections": 58,
            },
            {
                "name": "Redis",
                "role": "Cache",
                "status": "healthy",
                "storage_gb": 1.1,
                "connections": 14,
            },
        ],
        "analytics": {
            "open_rate": 0.46,
            "click_rate": 0.23,
            "reply_rate": 0.14,
            "conversions": 5,
            "ab_tests": [
                {"name": "CTA copy", "winner": "Book a call", "uplift": 0.12},
                {"name": "Send time", "winner": "09:00", "uplift": 0.08},
            ],
        },
        "feedback": [
            {
                "name": "Post-demo pulse",
                "question": "How clear was the value prop?",
                "last_sent": _today_iso(),
                "responses": 12,
            },
            {
                "name": "Onboarding check-in",
                "question": "Did you activate the core workflow?",
                "last_sent": _today_iso(),
                "responses": 8,
            },
        ],
        "actions": [
            {"title": "A/B test CTA for New Leads", "due": _today_iso(), "owner": "You"},
            {"title": "Send nurture to Dormant Accounts", "due": tomorrow.isoformat(), "owner": "You"},
            {"title": "Sync CRM deal stages", "due": tomorrow.isoformat(), "owner": "You"},
        ],
        "automation_rules": {
            "SMB_CTO": {"segment": "Tech Leads", "cadence": "0-3-7", "channel": "Email+LinkedIn"},
            "Enterprise": {"segment": "VP Sales", "cadence": "0-5-14-30", "ab_tests": 3},
            "Demo_video": {"variants": 2, "length": 90, "format": "MP4 vertical"},
        },
    }


def load_state() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        return reset_state()
    try:
        with DATA_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return reset_state()


def save_state(state: Dict[str, Any]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def reset_state() -> Dict[str, Any]:
    state = sample_state()
    save_state(state)
    return state


def _status_color(status: str) -> str:
    mapping = {
        "running": "green",
        "scheduled": "cyan",
        "ready": "yellow",
        "paused": "red",
        "connected": "green",
        "healthy": "green",
        "degraded": "yellow",
        "maintenance": "magenta",
        "pending": "yellow",
        "offline": "red",
        "failed": "red",
    }
    return mapping.get(status.lower(), "white")


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def build_campaign_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Automation",
        box=box.SIMPLE_HEAVY,
        expand=True,
        border_style=COLOR_ACCENT_CYAN,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_CYAN}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Name")
    table.add_column("Segment")
    table.add_column("Trigger")
    table.add_column("Channel")
    table.add_column("Template")
    table.add_column("Next")
    table.add_column("Status")
    for campaign in state.get("campaigns", []):
        status_value = campaign.get("status", "unknown")
        status = Text(status_value.title(), style=_status_color(status_value))
        table.add_row(
            campaign.get("name", "—"),
            campaign.get("segment", "—"),
            campaign.get("trigger", "—"),
            campaign.get("channel", "—"),
            campaign.get("template", "—"),
            campaign.get("next_send", "—"),
            status,
        )
    return table


def build_segment_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Segments",
        box=box.MINIMAL_HEAVY_HEAD,
        expand=True,
        border_style=COLOR_ACCENT_PURPLE,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_PURPLE}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Name")
    table.add_column("Criteria")
    table.add_column("Size", justify="right")
    for segment in state.get("segments", []):
        table.add_row(
            segment.get("name", "—"),
            "\n".join(f"• {c}" for c in segment.get("criteria", [])),
            str(segment.get("size", "—")),
        )
    return table


def build_template_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Creation Studio",
        box=box.MINIMAL_DOUBLE_HEAD,
        expand=True,
        border_style=COLOR_ACCENT_GREEN,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_GREEN}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Template")
    table.add_column("Medium")
    table.add_column("Purpose")
    table.add_column("Updated")
    for template in state.get("templates", []):
        table.add_row(
            template.get("name", "—"),
            template.get("medium", "—"),
            template.get("purpose", "—"),
            template.get("last_updated", "—"),
        )
    return table


def build_integration_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Connectors",
        box=box.SIMPLE,
        expand=True,
        border_style=COLOR_ACCENT_CYAN,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_CYAN}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("System")
    table.add_column("Status")
    table.add_column("Last Sync")
    table.add_column("Detail")
    connectors = state.get("connectors")
    # Support older saved states that only tracked integrations.
    if connectors is None:
        connectors = state.get("integrations", [])
    for connector in connectors:
        status = connector.get("status", "unknown")
        table.add_row(
            connector.get("name", "—"),
            Text(status.title(), style=_status_color(status)),
            connector.get("last_sync", "—"),
            connector.get("detail", "—"),
        )
    return table


def build_backend_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Backend Services",
        box=box.SIMPLE,
        expand=True,
        border_style=COLOR_ACCENT_PURPLE,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_PURPLE}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Service")
    table.add_column("Status")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Errors")
    table.add_column("Version")
    for service in state.get("backend", []):
        status = service.get("status", "unknown")
        table.add_row(
            service.get("service", "—"),
            Text(status.title(), style=_status_color(status)),
            str(service.get("latency_ms", "—")),
            str(service.get("error_rate", "—")),
            service.get("version", "—"),
        )
    return table


def build_database_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Databases",
        box=box.SIMPLE,
        expand=True,
        border_style=COLOR_ACCENT_GREEN,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_GREEN}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Name")
    table.add_column("Role")
    table.add_column("Status")
    table.add_column("Storage (GB)", justify="right")
    table.add_column("Connections", justify="right")
    for db in state.get("databases", []):
        status = db.get("status", "unknown")
        table.add_row(
            db.get("name", "—"),
            db.get("role", "—"),
            Text(status.title(), style=_status_color(status)),
            str(db.get("storage_gb", "—")),
            str(db.get("connections", "—")),
        )
    return table


def build_feedback_table(state: Dict[str, Any]) -> Table:
    table = Table(
        title="Feedback & Surveys",
        box=box.SIMPLE,
        expand=True,
        border_style=COLOR_ACCENT_CYAN,
        style=BACKGROUND_STYLE,
        header_style="bold white",
        title_style=f"bold {COLOR_ACCENT_CYAN}",
        row_styles=GLASS_ROW_STYLES,
    )
    table.add_column("Name")
    table.add_column("Question")
    table.add_column("Last Sent")
    table.add_column("Responses", justify="right")
    for form in state.get("feedback", []):
        table.add_row(
            form.get("name", "—"),
            form.get("question", "—"),
            form.get("last_sent", "-"),
            str(form.get("responses", "-")),
        )
    return table


def build_analytics_panel(state: Dict[str, Any]) -> Panel:
    analytics = state.get("analytics", {})
    lines = [
        f"Open rate: {format_pct(analytics.get('open_rate', 0))}",
        f"Click rate: {format_pct(analytics.get('click_rate', 0))}",
        f"Reply rate: {format_pct(analytics.get('reply_rate', 0))}",
        f"Conversions this week: {analytics.get('conversions', 0)}",
    ]
    ab_tests = analytics.get("ab_tests", [])
    if ab_tests:
        lines.append("A/B tests:")
        for test in ab_tests:
            lines.append(
                f" • {test.get('name', '—')} winner: {test.get('winner', '—')} (+{format_pct(test.get('uplift', 0))})"
            )
    body = "\n".join(lines)
    return Panel(
        body,
        title="Analytics & A/B Tests",
        box=box.ROUNDED,
        border_style=COLOR_ACCENT_AMBER,
        style=BACKGROUND_STYLE,
        title_align="left",
        padding=(1, 2),
    )


def build_actions_panel(state: Dict[str, Any]) -> Panel:
    actions = state.get("actions", [])
    if not actions:
        return Panel(
            "You're all set for today.",
            title="Today's Focus",
            box=box.ROUNDED,
            border_style=COLOR_ACCENT_AMBER,
            style=BACKGROUND_STYLE,
            padding=(1, 2),
        )
    lines = [f"• {item.get('title', 'Untitled')} (due {item.get('due', '—')})" for item in actions]
    return Panel(
        "\n".join(lines),
        title="Today's Focus",
        box=box.ROUNDED,
        border_style=COLOR_ACCENT_AMBER,
        style=BACKGROUND_STYLE,
        padding=(1, 2),
    )


def render_dashboard(state: Dict[str, Any], console: Console, now: datetime | None = None) -> None:
    now = now or datetime.now()
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=6),
    )
    layout["body"].split_row(Layout(name="left"), Layout(name="right"))
    layout["left"].split_column(Layout(name="campaigns"), Layout(name="segments"))
    layout["right"].split_column(Layout(name="templates"), Layout(name="analytics"))

    profile = state.get("profile", {})
    business_name = profile.get("business_name", "B2B Dashboard")
    header_text = Text(
        f"✦ {business_name} • B2B Engagement Command Center",
        style="bold #e2e8f0",
        justify="center",
    )
    subtitle = Text(f"{profile.get('owner', 'Owner')} • Updated {now.strftime(DATETIME_HEADER_FMT)}", style=STYLE_MUTED)
    layout["header"].update(
        Panel(
            Align.center(header_text),
            subtitle_align="right",
            subtitle=subtitle,
            border_style=COLOR_ACCENT_AMBER,
            box=box.ROUNDED,
            style=BACKGROUND_STYLE,
            padding=(0, 2),
        )
    )

    layout["campaigns"].update(build_campaign_table(state))
    layout["segments"].update(build_segment_table(state))
    layout["templates"].update(build_template_table(state))
    layout["analytics"].update(build_analytics_panel(state))

    footer_layout = Layout()
    footer_layout.split_column(
        Layout(name="footer_top"),
        Layout(name="footer_bottom"),
    )
    footer_layout["footer_top"].split_row(
        Layout(name="connectors"),
        Layout(name="backend"),
        Layout(name="database"),
    )
    footer_layout["footer_bottom"].split_row(
        Layout(name="feedback"),
        Layout(name="actions"),
    )
    footer_layout["connectors"].update(build_integration_table(state))
    footer_layout["backend"].update(build_backend_table(state))
    footer_layout["database"].update(build_database_table(state))
    footer_layout["feedback"].update(build_feedback_table(state))
    footer_layout["actions"].update(build_actions_panel(state))
    layout["footer"].update(footer_layout)

    console.print(layout)


def generate_auto_plan(creative_idea: str) -> Dict[str, Any]:
    """
    Match user's creative idea to automation rules and generate a plan.
    Uses simple keyword matching to determine which rule to apply.
    """
    idea_lower = creative_idea.lower()
    
    # Define keyword patterns for each rule
    rule_patterns = {
        "SMB_CTO": ["smb", "cto", "tech lead", "technical", "small business", "medium business"],
        "Enterprise": ["enterprise", "vp", "sales", "large", "corporation"],
        "Demo_video": ["demo", "video", "presentation", "recording", "mp4"],
    }
    
    # Find the best matching rule
    matched_rule = None
    for rule_name, keywords in rule_patterns.items():
        if any(keyword in idea_lower for keyword in keywords):
            matched_rule = rule_name
            break
    
    # Default plan if no match found
    default_plan = {
        "rule_matched": "Default",
        "segment": "General Audience",
        "cadence": "0-7",
        "channel": "Email",
        "variants": 1,
        "auto_handled": ["Segment selection", "Basic scheduling"],
    }
    
    if not matched_rule:
        return default_plan
    
    # Load the actual rules from sample state
    state = sample_state()
    rules = state.get("automation_rules", {})
    rule_config = rules.get(matched_rule, {})
    
    # Build the auto plan
    auto_plan = {
        "rule_matched": matched_rule,
        "segment": rule_config.get("segment", "General Audience"),
        "cadence": rule_config.get("cadence", "0-7"),
        "channel": rule_config.get("channel", "Email"),
        "variants": rule_config.get("variants", 1),
        "ab_tests": rule_config.get("ab_tests"),
        "length": rule_config.get("length"),
        "format": rule_config.get("format"),
        "auto_handled": [],
    }
    
    # Track what was auto-handled
    if auto_plan.get("segment"):
        auto_plan["auto_handled"].append(f"Segment: {auto_plan['segment']}")
    if auto_plan.get("cadence"):
        auto_plan["auto_handled"].append(f"Cadence: {auto_plan['cadence']} days")
    if auto_plan.get("channel"):
        auto_plan["auto_handled"].append(f"Channel: {auto_plan['channel']}")
    if auto_plan.get("ab_tests"):
        auto_plan["auto_handled"].append(f"A/B tests: {auto_plan['ab_tests']} variants")
    if auto_plan.get("variants"):
        auto_plan["auto_handled"].append(f"Creative variants: {auto_plan['variants']}")
    if auto_plan.get("length"):
        auto_plan["auto_handled"].append(f"Video length: {auto_plan['length']}s")
    if auto_plan.get("format"):
        auto_plan["auto_handled"].append(f"Format: {auto_plan['format']}")
    
    return auto_plan


def render_creative_studio(creative_idea: str, auto_plan: Dict[str, Any], console: Console) -> None:
    """
    Render the Creative Studio UI with a 70/30 split layout.
    Left (70%): Creation Studio for editing content
    Right (30%): Auto-magic status showing what was handled automatically
    """
    layout = Layout()
    layout.split_row(
        Layout(name="studio", ratio=70),
        Layout(name="automagic", ratio=30),
    )
    
    # Build the Creation Studio panel (left side - 70%)
    studio_content = []
    studio_content.append(f"[bold {COLOR_ACCENT_CYAN}]Your Creative Idea:[/bold {COLOR_ACCENT_CYAN}]")
    studio_content.append(f"  {creative_idea}")
    studio_content.append("")
    studio_content.append(f"[bold {COLOR_ACCENT_GREEN}]Script (editable):[/bold {COLOR_ACCENT_GREEN}]")
    studio_content.append("  → Opening hook: Grab attention in first 3 seconds")
    studio_content.append("  → Problem statement: What pain point are we solving?")
    studio_content.append("  → Solution demo: Show the product in action")
    studio_content.append("  → Call to action: Book a demo / Start trial")
    studio_content.append("")
    studio_content.append(f"[bold {COLOR_ACCENT_PURPLE}]Thumbnails:[/bold {COLOR_ACCENT_PURPLE}]")
    studio_content.append("  [Thumbnail A] Bold text with product screenshot")
    studio_content.append("  [Thumbnail B] Face + emotion-driven design")
    studio_content.append("")
    studio_content.append(f"[bold {COLOR_ACCENT_AMBER}]Voiceover:[/bold {COLOR_ACCENT_AMBER}]")
    studio_content.append("  Professional voice (auto-generated available)")
    studio_content.append("")
    studio_content.append(f"[bold {COLOR_ACCENT_GREEN}]Actions:[/bold {COLOR_ACCENT_GREEN}]")
    studio_content.append("  [Launch] Deploy campaign (segments, timing, syncs handled)")
    studio_content.append("  [Preview] See how it looks across channels")
    studio_content.append("  [Edit] Modify script, thumbnails, or voiceover")
    
    studio_panel = Panel(
        "\n".join(studio_content),
        title="Creation Studio",
        box=box.ROUNDED,
        border_style=COLOR_ACCENT_CYAN,
        style=BACKGROUND_STYLE,
        padding=(1, 2),
    )
    
    # Build the Auto-magic Status panel (right side - 30%)
    auto_content = []
    auto_content.append(f"[bold {COLOR_ACCENT_PURPLE}]Rule Matched:[/bold {COLOR_ACCENT_PURPLE}]")
    auto_content.append(f"  {auto_plan.get('rule_matched', 'None')}")
    auto_content.append("")
    auto_content.append(f"[bold {COLOR_ACCENT_GREEN}]Auto-handled:[/bold {COLOR_ACCENT_GREEN}]")
    
    auto_handled = auto_plan.get("auto_handled", [])
    if auto_handled:
        for item in auto_handled:
            auto_content.append(f"  ✓ {item}")
    else:
        auto_content.append("  (none)")
    
    auto_content.append("")
    auto_content.append(f"[bold {COLOR_ACCENT_AMBER}]Status:[/bold {COLOR_ACCENT_AMBER}]")
    auto_content.append("  ✓ Segments configured")
    auto_content.append("  ✓ Scheduling ready")
    auto_content.append("  ✓ Syncs prepared")
    auto_content.append("  → Ready to launch!")
    
    auto_panel = Panel(
        "\n".join(auto_content),
        title="Auto-magic Status",
        box=box.ROUNDED,
        border_style=COLOR_ACCENT_AMBER,
        style=BACKGROUND_STYLE,
        padding=(1, 2),
    )
    
    layout["studio"].update(studio_panel)
    layout["automagic"].update(auto_panel)
    
    # Print header
    header_text = Text(
        "✦ Creative Mode • Easy Campaign Creation",
        style="bold #e2e8f0",
        justify="center",
    )
    header_panel = Panel(
        Align.center(header_text),
        border_style=COLOR_ACCENT_AMBER,
        box=box.ROUNDED,
        style=BACKGROUND_STYLE,
        padding=(0, 2),
    )
    console.print(header_panel)
    console.print()
    console.print(layout)
    console.print()
    console.print(f"[dim]The system has handled the dirty work (segments, scheduling, syncs) automatically.[/dim]")
    console.print(f"[{COLOR_ACCENT_GREEN}]Press Launch when ready to deploy your campaign![/{COLOR_ACCENT_GREEN}]")


def creative_mode(console: Console) -> None:
    """
    Handle the creative mode workflow.
    Prompts user for a creative idea, generates an auto plan, and renders the studio.
    """
    creative_idea = Prompt.ask("What's your creative idea?")
    auto_plan = generate_auto_plan(creative_idea)
    render_creative_studio(creative_idea, auto_plan, console)


def add_campaign(args: argparse.Namespace, state: Dict[str, Any]) -> None:
    campaigns: List[Dict[str, Any]] = state.setdefault("campaigns", [])
    campaigns.append(
        {
            "name": args.name,
            "segment": args.segment,
            "trigger": args.trigger,
            "channel": args.channel,
            "template": args.template,
            "status": args.status,
            "next_send": args.next_send or _today_iso(),
        }
    )
    save_state(state)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Desktop-style dashboard for B2B customer engagement."
    )
    parser.add_argument("--summary", action="store_true", help="Show dashboard summary.")
    parser.add_argument("--snapshot", action="store_true", help="Export dashboard SVG.")
    parser.add_argument(
        "--snapshot-path",
        type=Path,
        default=DEFAULT_SNAPSHOT_PATH,
        help="Where to save the SVG snapshot.",
    )
    parser.add_argument("--reset-sample", action="store_true", help="Restore sample data.")
    parser.add_argument("--creative-mode", action="store_true", help="Launch Creative Mode for easy campaign creation.")
    parser.add_argument("--add-campaign", action="store_true", help="Add a new automation.")
    parser.add_argument("--name", help="Campaign name when adding automation.")
    parser.add_argument("--segment", help="Target segment for automation.")
    parser.add_argument("--trigger", help="Trigger condition.")
    parser.add_argument("--channel", help="Primary channel.")
    parser.add_argument("--template", help="Template name to use.")
    parser.add_argument(
        "--status",
        choices=["scheduled", "ready", "running", "paused"],
        default="scheduled",
        help="Initial campaign status (default: scheduled).",
    )
    parser.add_argument(
        "--next-send",
        dest="next_send",
        help="Next send date (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


def ensure_valid_campaign_args(args: argparse.Namespace) -> None:
    required = {
        "name": args.name,
        "segment": args.segment,
        "trigger": args.trigger,
        "channel": args.channel,
        "template": args.template,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise SystemExit(f"Missing required fields for campaign: {', '.join(missing)}")


def validate_next_send(next_send: str | None) -> str | None:
    if not next_send:
        return None
    try:
        datetime.strptime(next_send, "%Y-%m-%d")
        return next_send
    except ValueError:
        raise SystemExit("Invalid --next-send date. Use YYYY-MM-DD.")


def should_render_dashboard(args: argparse.Namespace) -> bool:
    if args.summary or args.snapshot:
        return True
    # Default to rendering the dashboard when no mutating actions are requested.
    return not any([args.add_campaign, args.reset_sample, args.creative_mode])


def main() -> None:
    args = parse_args()
    state = load_state()

    args.next_send = validate_next_send(args.next_send)

    if args.reset_sample:
        state = reset_state()

    if args.add_campaign:
        ensure_valid_campaign_args(args)
        add_campaign(args, state)

    console = themed_console(record=args.snapshot)

    if args.creative_mode:
        creative_mode(console)
        return

    render_time = datetime.now()

    if should_render_dashboard(args):
        render_dashboard(state, console, now=render_time)

    if args.snapshot:
        args.snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        console.save_svg(str(args.snapshot_path), title="B2B Engagement Dashboard")
        status_console = themed_console()
        status_console.print(f"Saved snapshot to {args.snapshot_path}")


if __name__ == "__main__":
    main()
