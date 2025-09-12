"""CLI entrypoint shim mapping to internal toolbox."""
from tools.cli.toolbox_cli import main  # re-export
__all__ = ["main"]
