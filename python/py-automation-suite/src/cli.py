import typer

from src.scripts.script1 import app as script1
from src.scripts.script2 import app as script2

app = typer.Typer(
    name="Automation Scripts",
    help="Central CLI for Automations",
    no_args_is_help=True,
)


# Router for script
app.add_typer(script1, name="", help="")
app.add_typer(script2, name="", help="")

if __name__ == "__main__":
    app()
