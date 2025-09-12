"""DailyAssistant public package wrapper.

Provides a stable import surface layering over the internal 'tools' directory
without forcing a mass rename. External consumers should prefer:

    import dailyassistant
    from dailyassistant.google.docs.api import append_llm_plan_to_doc

while legacy code inside this repository can continue to use 'tools.*' until
fully migrated.
"""
from importlib import import_module as _im

# Re-export structured subpackages if present.
_tools = _im("tools")

google = getattr(_tools, "google", None)
email = getattr(_tools, "email", None)
openrouter = getattr(_tools, "openrouter", None)
pdf = getattr(_tools, "pdf", None)
cli = getattr(_tools, "cli", None)
misc = getattr(_tools, "misc", None)

__all__ = [
    name for name, val in {
        "google": google,
        "email": email,
        "openrouter": openrouter,
        "pdf": pdf,
        "cli": cli,
        "misc": misc,
    }.items() if val is not None
]
