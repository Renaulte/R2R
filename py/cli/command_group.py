import click

from sdk.client import R2RClient


@click.group()
@click.option(
    "--base-url", default="http://localhost:8000", help="Base URL for the API"
)
@click.option("--json", is_flag=True, help="Output in JSON format")
@click.pass_context
def cli(ctx, base_url, json):
    """R2R CLI for all core operations."""
    client = R2RClient(base_url=base_url)
    client.json = json
    ctx.obj = client
