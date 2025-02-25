import importlib
from typing import Optional

import typer
from typer import Typer

from wcgw_cli.anthropic_client import loop as claude_loop
from wcgw_cli.openai_client import loop as openai_loop

app = Typer(pretty_exceptions_show_locals=False)


@app.command()
def loop(
    claude: bool = False,
    first_message: Optional[str] = None,
    limit: Optional[float] = None,
    resume: Optional[str] = None,
    version: bool = typer.Option(False, "--version", "-v"),
) -> tuple[str, float]:
    if version:
        version_ = importlib.metadata.version("wcgw")
        print(f"wcgw version: {version_}")
        exit()
    if claude:
        return claude_loop(
            first_message=first_message,
            limit=limit,
            resume=resume,
        )
    else:
        return openai_loop(
            first_message=first_message,
            limit=limit,
            resume=resume,
        )


if __name__ == "__main__":
    app()
