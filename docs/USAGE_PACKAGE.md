# DailyAssistant Package Usage

## Install (Editable for Local Development)
```bash
pip install -e .[all]
```

Or minimal core (no extras):
```bash
pip install -e .
```

## Import Examples
```python
from dailyassistant.google.docs.api.append_llm_plan_to_doc import main as append_plan
from dailyassistant.openrouter.llm_common import chat_with_fallback
```

## CLI
After installation a `da` command is available:
```bash
da pdf:to-clean-md --input sample.pdf --output-clean sample_clean.md
```

## Extras
| Extra | Purpose |
|-------|---------|
| google | Google Docs/Slides/Drive APIs |
| email  | Email parsing & workflows |
| pdf    | PDF → Markdown + cleaning |
| openrouter | LLM client helpers |
| all    | Everything above |

Install a subset:
```bash
pip install -e .[google,pdf]
```

## Configuration
Credentials & tokens are NOT packaged. Place them in project directories or a config path you manage (e.g. `projects/<name>/secrets/`). Your code loads them by path.

## Migration Notes
Legacy imports like `from operating.GoogleDocsAPI.append_llm_plan_to_doc import main` should migrate to:
```python
from dailyassistant.google.docs.api.append_llm_plan_to_doc import main
```

Temporary compatibility comes via the existing `tools` namespace; remove usage over time.
