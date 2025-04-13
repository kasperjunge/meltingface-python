# Melting Face 🫠 

A Python SDK that allows you to load prompts hosted on [meltingface.eu](https://meltingface.eu). The library handles:

- Simple **prompt** objects (`Prompt`)  
- **Fetching** public and private prompts from the MeltingFace hub  
- **Caching** to avoid repeated downloads  

## Installation

```bash
pip install meltingface
```

## Basic Usage

### Loading a Public Prompt

```python
from meltingface.prompt import Prompt

# Load a prompt from the public hub
prompt = Prompt.from_hub("owner/repo", version="0.1.0")

print(prompt.text)   # -> "Hello from my prompt!"
print(prompt.version) # -> "v1"
```

### Loading a Private Prompt

Private prompts require authentication with an API key:

```python
from meltingface.prompt import Prompt

# Option 1: Pass the API key directly
prompt = Prompt.from_hub("owner/private-repo", api_key="your-api-key")

# Option 2: Set the MELTINGFACE_API_KEY environment variable
# export MELTINGFACE_API_KEY="your-api-key"
prompt = Prompt.from_hub("owner/private-repo")
```

## API Reference

- **`repo_id`** (`"owner/repo"`) is how you reference your prompt's repository on meltingface.eu
- **`version`** is optional; if not provided, the library defaults to `"latest"`
- **`api_key`** is required for private prompts; can be passed directly or via the MELTINGFACE_API_KEY environment variable
- **`cache_dir`** lets you specify a custom cache location (defaults to ~/.meltingface/prompts)
- **`force_download`** when set to True, bypasses the cache and fetches the prompt again
