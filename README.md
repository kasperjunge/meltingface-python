# Melting Face 🫠

A minimal Python SDK that allows you to load prompts hosted on [meltingface.eu](https://meltingface.eu). The library handles:

- Simple **prompt** objects (`Prompt`)  
- **Fetching** public prompts from the MeltingFace hub (via `from_hub`)  
- **Caching** to avoid repeated downloads  

## Installation

```bash
pip install meltingface
```

## Basic Usage

### Loading a Prompt

```python
from meltingface.prompt import Prompt

# Load a prompt from the public hub
prompt = Prompt.from_hub("owner/repo", version="0.0.1")

print(prompt.text)   # -> "Hello from my prompt!"
print(prompt.version) # -> "v1"
```

- **`repo_id`** (`"owner/repo"`) is how you reference your prompt’s repository on meltingface.eu.
- **`version`** is optional; if not provided, the library defaults to `"latest"`.
