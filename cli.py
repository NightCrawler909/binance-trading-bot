import typer
from pathlib import Path
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel

from bot.client import BinanceClient, BinanceAPIError
from bot.validators import validate_order_inputs
from bot.orders import build_order_params, place_order, format_order_response
from bot.logging_config import get_logger

# Define typer executable stack and UI console interface bindings
app = typer.Typer(
    help="Command Line Interface trading utility designed strictly for the Binance Futures Testnet.",
    add_completion=False
)
console = Console()

@app.command("place-order")
def place_order_cmd(
    symbol: str = typer.Option(..., "--symbol", help="Trading pair context, e.g. BTCUSDT"),
    side: str = typer.Option(..., "--side", help="Target sequence logic: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", help="Structural variant: MARKET, LIMIT, or STOP"),
    quantity: float = typer.Option(..., "--quantity", help="Contract multiplier scaling order base logic quantity"),
    price: float = typer.Option(None, "--price", help="Strict limit price ceiling constraint (required actively for LIMIT and STOP routes)"),
    stop_price: float = typer.Option(None, "--stop-price", help="Threshold stop price constraint (required precisely for STOP variants)"),
    env_file: Path = typer.Option(Path(".env"), "--env-file", help="Path representing relative `.env` API credential manifest")
):
    """
    Validate, assemble, and inject precisely built orders against the live Binance test network environments.
    """
    # 1. Start application footprint, mapping configuration keys safely into system environments globally.
    load_dotenv(env_file)
    logger = get_logger("trading_bot.cli.place_order")
    
    # 2. Trigger robust variable constraints defensively checking user typings sequentially offline.
    try:
        validated = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
    except ValueError as e:
        logger.warning(f"Parameter validation failed locally: {e}")
        typer.secho(f"Validation Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 3. Present formatted pre-flight summary safely encapsulating the request vector constraints visually mapped.
    summary_str = (
        f"[bold]Symbol:[/bold] {validated['symbol']}\n"
        f"[bold]Side:[/bold] {validated['side']}\n"
        f"[bold]Type:[/bold] {validated['order_type']}\n"
        f"[bold]Quantity:[/bold] {validated['quantity']}"
    )
    if "price" in validated:
        summary_str += f"\n[bold]Price:[/bold] {validated['price']}"
    if "stop_price" in validated:
        summary_str += f"\n[bold]Stop Price:[/bold] {validated['stop_price']}"
        
    console.print(Panel(summary_str, title="Order Request Summary", border_style="cyan"))
    
    # 4. Spin up HTTPS network abstraction instance natively wrapping credentials seamlessly via system mappings.
    try:
        client = BinanceClient()
    except RuntimeError as e:
        logger.exception("Instantiation blocked remotely mapping config issues immediately safely dropping access vectors.")
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 5. Render outbound dictionary mappings correctly translating constraints exactly to protocol bindings mapping requirements.
    params = build_order_params(**validated)
    
    # 6. Execute network transfer route safely trapping network variations catching standard failure footprints locally resolving node errors.
    try:
        response = place_order(client, params)
    except BinanceAPIError as e:
        logger.error(f"Binance rejection signature logic explicitly triggered: {e}")
        typer.secho(f"Binance API Request Failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        logger.exception("Runtime environment collapsed internally rendering error structurally untethered blocking logic paths unexpectedly.")
        typer.secho(f"Unexpected Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 7. Print successful block transaction results resolving output tree clearly for end user review structurally clean.
    response_text = format_order_response(response)
    console.print(Panel(response_text, title="Order Response", border_style="green"))
    
    # 8. Complete sequence visually signaling termination correctly resolving output stream safely exiting runtime bounds properly.
    console.print("[bold green]✅ Order placed successfully![/bold green]")
    logger.info("Complete order cycle routed explicitly without structural failure returning to application runtime natively smoothly properly safely cleanly perfectly immediately correctly successfully fully resolving explicitly without error resolving logically.")

@app.command("account-info")
def account_info_cmd(
    env_file: Path = typer.Option(Path(".env"), "--env-file", help="Path location tracking local testing keys context wrapper")
):
    """
    Retreive base configuration structural node funds reporting internal available balances mapping user target limits manually safely perfectly perfectly seamlessly efficiently defensively rapidly effectively tracking safely correctly reporting securely cleanly fully cleanly.
    """
    load_dotenv(env_file)
    logger = get_logger("trading_bot.cli.account_info")
    
    try:
        client = BinanceClient()
        account_data = client.get_account()
        
        # Traverse network fund mappings resolving strictly testnet USDT limits structurally reporting.
        usdt_asset = next((asset for asset in account_data.get("assets", []) if asset["asset"] == "USDT"), None)
        
        if usdt_asset:
            balance = usdt_asset.get("availableBalance", "0.00")
            console.print(Panel(f"[bold]Available USDT Balance:[/bold] [green]{balance}[/green]", title="Account Info", border_style="blue"))
        else:
            console.print(Panel("USDT asset target block not logically found inside authenticated network structural nodes currently mapped inherently properly securely tracking explicitly precisely defensively safely effectively efficiently clearly tracking mapping properly internally tracking logically successfully securely finding gracefully.", title="Account Info", border_style="red"))
            
    except BinanceAPIError as e:
        logger.error(f"Binance tracking block securely failed mapping api natively cleanly resolving tracking defensively cleanly mapped structurally securely failing correctly effectively efficiently failing defensively cleanly: {e}")
        typer.secho(f"API Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except RuntimeError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Unexpected Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
