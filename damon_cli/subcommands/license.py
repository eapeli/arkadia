"""
License subcommand for Damon CLI
"""
from __future__ import annotations

import asyncio
import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from damon_cli.subcommands._shared import (
    console,
    print_success,
    print_error,
    print_warning,
    print_info,
    load_cli_config,
    save_config_value,
)

app = typer.Typer(
    name="license",
    help="License & subscription management",
    no_args_is_help=True,
)

console = Console()


def get_license_client():
    """Get or create license client"""
    from damon_license import get_license_client as _get_client
    return _get_client()


@app.command("activate")
def license_activate(
    key: Optional[str] = typer.Argument(None, help="License key to activate"),
    offline: bool = typer.Option(False, "--offline", "-o", help="Activate offline (manual entry)"),
):
    """Activate a license key"""
    client = get_license_client()

    if not key:
        if offline:
            key = Prompt.ask("Enter license key")
        else:
            console.print(Panel(
                "Enter your license key to activate Damon Agent.\n"
                "Get a key at: https://damon-agent.dev/pricing",
                title="License Activation",
                border_style="blue",
            ))
            key = Prompt.ask("License key")

    if not key:
        print_error("No license key provided")
        raise typer.Exit(1)

    console.print(f"Activating license: [cyan]{key[:20]}...[/cyan]")

    try:
        result = asyncio.run(client.validate_online(key))

        if result.valid:
            print_success(f"License activated successfully!")
            console.print(f"  Tier: [green]{result.license.tier.value}[/green]")
            console.print(f"  Email: [cyan]{result.license.user_email}[/cyan]")
            if result.license.expires_at:
                console.print(f"  Expires: [yellow]{result.license.expires_at.strftime('%Y-%m-%d')}[/yellow]")
            else:
                console.print(f"  Expires: [green]Never[/green]")

            # Save key for future validations
            client.save_license_key(key)
        else:
            print_error(f"Activation failed: {result.error}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Activation error: {e}")
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            print_warning("Could not reach license server. Trying offline validation...")
            offline_result = client.validate_offline()
            if offline_result.valid:
                print_success("Offline validation succeeded (cached license)")
                console.print(f"  Tier: [green]{offline_result.license.tier.value}[/green]")
            else:
                print_error("Offline validation also failed")
                raise typer.Exit(1)
            raise typer.Exit(1)
        raise typer.Exit(1)


@app.command("status")
def license_status(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    offline: bool = typer.Option(False, "--offline", "-o", help="Use cached license only"),
):
    """Check license status"""
    client = get_license_client()

    if offline:
        result = client.validate_offline()
    else:
        result = asyncio.run(client.validate())

    if json_output:
        console.print_json(data={
            "valid": result.valid,
            "tier": result.license.tier.value if result.license else "free",
            "status": result.license.status.value if result.license else "inactive",
            "email": result.license.user_email if result.license else None,
            "expires_at": result.license.expires_at.isoformat() if result.license and result.license.expires_at else None,
            "expires_in_days": result.expires_in_days,
            "features": result.features.model_dump() if result.features else {},
            "error": result.error,
        })
        return

    if result.valid:
        license = result.license
        tier_color = {
            "free": "dim",
            "starter": "blue",
            "professional": "green",
            "team": "cyan",
            "enterprise": "magenta",
        }.get(license.tier.value, "white")

        console.print(Panel(
            f"[bold]Tier:[/bold] [{tier_color}]{license.tier.value.upper()}[/{tier_color}]\n"
            f"[bold]Status:[/bold] [green]{license.status.value.upper()}[/green]\n"
            f"[bold]Email:[/bold] {license.user_email}\n"
            f"[bold]Key:[/bold] {license.key[:20]}...\n"
            f"[bold]Expires:[/bold] {license.expires_at.strftime('%Y-%m-%d') if license.expires_at else 'Never'}"
            + (f"\n[bold]Days Remaining:[/bold] {result.expires_in_days}" if result.expires_in_days is not None else ""),
            title="License Status: VALID",
            border_style="green",
        ))

        if result.features:
            features_table = Table(title="Enabled Features", show_header=True, header_style="bold")
            features_table.add_column("Feature")
            features_table.add_column("Value")

            for field, value in result.features.model_dump().items():
                if isinstance(value, list):
                    value = ", ".join(value) if value else "None"
                features_table.add_row(field.replace("_", " ").title(), str(value))

            console.print(features_table)
    else:
        console.print(Panel(
            f"[bold red]License Invalid[/bold red]\n\n{result.error}",
            title="License Status: INVALID",
            border_style="red",
        ))
        raise typer.Exit(1)


@app.command("deactivate")
def license_deactivate():
    """Deactivate current license (clear local cache)"""
    client = get_license_client()

    if Confirm.ask("Are you sure you want to deactivate this license locally?"):
        client.clear_license_key()
        print_success("License deactivated locally")
        print_info("Note: This does not cancel your subscription. Use the billing portal for that.")
    else:
        print_info("Cancelled")


@app.command("info")
def license_info():
    """Show detailed license information"""
    client = get_license_client()
    info = client.get_license_info()

    console.print(Panel(
        f"[bold]Status:[/bold] {info['status']}\n"
        f"[bold]Tier:[/bold] {info['tier']}\n"
        f"[bold]Key:[/bold] {info['key']}\n"
        f"[bold]Email:[/bold] {info['email']}\n"
        f"[bold]Expires:[/bold] {info['expires']}",
        title="License Information",
        border_style="blue",
    ))

    if "features" in info:
        features_table = Table(title="Features", show_header=True)
        features_table.add_column("Feature")
        features_table.add_column("Value")
        for k, v in info["features"].items():
            features_table.add_row(k.replace("_", " ").title(), str(v))
        console.print(features_table)


@app.command("portal")
def license_portal():
    """Open Stripe billing portal to manage subscription"""
    client = get_license_client()
    key = client.load_license_key()

    if not key:
        print_error("No license key found. Activate a license first.")
        raise typer.Exit(1)

    console.print("Opening billing portal...")

    try:
        from damon_license.client import DamonLicenseClient
        # We need the server URL - get from config or use default
        portal_url = asyncio.run(_create_portal_session(key))
        console.print(f"Opening: [link]{portal_url}[/link]")
        import webbrowser
        webbrowser.open(portal_url)
    except Exception as e:
        print_error(f"Failed to open portal: {e}")
        raise typer.Exit(1)


async def _create_portal_session(key: str) -> str:
    """Create billing portal session via license server"""
    import httpx
    from damon_license.client import DamonLicenseClient

    client = DamonLicenseClient()
    # Call the server's portal endpoint
    async with httpx.AsyncClient() as http:
        resp = await http.post(
            f"{client.server_url}/api/v1/license/portal",
            json={"license_key": key},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["url"]


@app.command("checkout")
def license_checkout(
    tier: str = typer.Argument(..., help="Tier: starter, professional, team, enterprise"),
    interval: str = typer.Option("monthly", "--interval", "-i", help="Billing interval: monthly or yearly"),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email for account"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Name for account"),
):
    """Create checkout session for new subscription"""
    from damon_license.models import LicenseTier, BillingInterval

    try:
        tier_enum = LicenseTier(tier.lower())
    except ValueError:
        print_error(f"Invalid tier: {tier}. Options: {[t.value for t in LicenseTier]}")
        raise typer.Exit(1)

    try:
        interval_enum = BillingInterval(interval.lower())
    except ValueError:
        print_error(f"Invalid interval: {interval}. Options: monthly, yearly")
        raise typer.Exit(1)

    if not email:
        email = Prompt.ask("Email address")

    console.print(f"Creating checkout for [bold]{tier_enum.value}[/bold] ({interval_enum.value})...")

    try:
        from damon_license.client import DamonLicenseClient
        import httpx

        client = DamonLicenseClient()
        async with httpx.AsyncClient() as http:
            resp = await http.post(
                f"{client.server_url}/api/v1/license/checkout",
                json={
                    "tier": tier_enum.value,
                    "interval": interval_enum.value,
                    "email": email,
                    "name": name,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()

        console.print(f"Checkout URL: [link]{data['url']}[/link]")
        print_info("Complete payment to activate your subscription")

        if Confirm.ask("Open in browser now?"):
            import webbrowser
            webbrowser.open(data["url"])

    except Exception as e:
        print_error(f"Checkout failed: {e}")
        raise typer.Exit(1)


@app.command("verify")
def license_verify(
    key: Optional[str] = typer.Argument(None, help="License key to verify"),
):
    """Verify a license key without activating"""
    client = get_license_client()

    if not key:
        key = Prompt.ask("License key to verify")

    result = asyncio.run(client.validate_online(key))

    if result.valid:
        print_success("License key is valid")
        console.print(f"  Tier: [green]{result.license.tier.value}[/green]")
        console.print(f"  Email: [cyan]{result.license.user_email}[/cyan]")
    else:
        print_error(f"License key is invalid: {result.error}")
        raise typer.Exit(1)