"""
Main CLI entry point for Cloud Service Manager.
"""

import json
from enum import Enum
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .providers.aws import AWSProvider
from .providers.azure import AzureProvider
from .providers.gcp import GCPProvider

app = typer.Typer(
    name="CloudServiceManager",
    help="Discover and manage cloud services across AWS, Azure, and GCP",
)

console = Console()


class OutputFormat(str, Enum):
    """Output format options."""
    JSON = "json"
    TABLE = "table"
    CSV = "csv"


class ProviderOption(str, Enum):
    """Provider selection options for list-services."""

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    ALL = "all"


@app.command()
def list_services(
    provider: ProviderOption = typer.Option(
        ProviderOption.ALL,
        "--provider",
        "-p",
        help="Cloud provider (aws, gcp, azure, or 'all')"
    ),
    region: Optional[str] = typer.Option(
        None,
        "--region",
        "-r",
        help="Filter by region (provider-specific)"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        "-f",
        help="Output format"
    ),
):
    """
    List cloud services from specified providers.
    
    Examples:
        cloudmgr list-services                    # All providers, table format
        cloudmgr list-services --provider aws     # AWS only
        cloudmgr list-services -p gcp -f json     # GCP, JSON format
        cloudmgr list-services --provider all -r us-east-1
    """
    try:
        providers = _get_providers(provider)
        
        # Fetch services from all specified providers
        all_services = []
        provider_errors = []
        for prov in providers:
            try:
                services = prov.list_services(region)
                all_services.extend(services)
            except Exception as e:
                provider_name = prov.__class__.__name__.replace("Provider", "").lower()
                provider_errors.append(f"{provider_name}: {e}")

        if provider_errors:
            for err in provider_errors:
                console.print(f"[yellow]Warning[/yellow]: failed to fetch from {err}")
        
        if not all_services:
            if provider_errors:
                raise RuntimeError("All requested providers failed")
            console.print("[yellow]No services found.[/yellow]")
            return
        
        # Output in requested format
        _output_services(all_services, format)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def get_service(
    provider: str = typer.Option(
        ...,
        "--provider",
        "-p",
        help="Cloud provider (aws, gcp, or azure)"
    ),
    service_id: str = typer.Option(
        ...,
        "--id",
        "-i",
        help="Service identifier"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.JSON,
        "--format",
        "-f",
        help="Output format"
    ),
):
    """Get details of a specific cloud service."""
    try:
        prov = _get_provider(provider)
        service = prov.get_service(service_id)
        
        if service is None:
            console.print("[yellow]Service not found.[/yellow]")
            return
        
        _output_services([service], format)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def init_config():
    """Initialize configuration for cloud credentials."""
    console.print("[cyan]Cloud Service Manager Configuration Setup[/cyan]")
    console.print()
    
    # TODO: Interactive configuration setup
    console.print("Please set up your cloud credentials:")
    console.print()
    console.print("AWS: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html")
    console.print("GCP: https://cloud.google.com/docs/authentication/getting-started")
    console.print("Azure: https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli")
    console.print()
    console.print("[green]Configuration Guide: See docs/SETUP.md[/green]")


def _get_providers(provider: ProviderOption = ProviderOption.ALL) -> list:
    """Get provider instances based on specification."""
    if provider == ProviderOption.ALL:
        return [AWSProvider(), GCPProvider(), AzureProvider()]
    
    return [_get_provider(provider.value)]


def _get_provider(provider: str):
    """Get a single provider instance."""
    provider_map = {
        "aws": AWSProvider,
        "gcp": GCPProvider,
        "azure": AzureProvider,
    }
    
    provider_class = provider_map.get(provider.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider}")
    
    return provider_class()


def _output_services(services, format: OutputFormat):
    """Output services in the specified format."""
    # Keep output deterministic for easier comparison and testing.
    sorted_services = sorted(
        services,
        key=lambda s: (str(s.provider), str(s.region), str(s.service_type), str(s.name)),
    )

    if format == OutputFormat.JSON:
        output = [s.to_dict() for s in sorted_services]
        console.print_json(json.dumps(output, indent=2))
    
    elif format == OutputFormat.TABLE:
        table = Table(title="Cloud Services")
        table.add_column("Provider", style="cyan")
        table.add_column("Service Type", style="magenta")
        table.add_column("Name", style="green")
        table.add_column("Region", style="yellow")
        table.add_column("Status", style="blue")
        
        for service in sorted_services:
            table.add_row(
                service.provider,
                service.service_type,
                service.name,
                service.region,
                service.status,
            )
        
        console.print(table)
    
    elif format == OutputFormat.CSV:
        import csv
        import io
        
        output = io.StringIO()
        if sorted_services:
            csv_rows = [service.to_csv_dict() for service in sorted_services]
            writer = csv.DictWriter(output, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)
        
        console.print(output.getvalue())


if __name__ == "__main__":
    app()
