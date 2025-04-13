# MeltingFace SDK Examples

This directory contains examples that demonstrate how to use the MeltingFace Python SDK.

## Available Examples

### basic_usage.py

A simple example that shows how to:
- Load a prompt from the MeltingFace hub
- Access the prompt text
- View prompt metadata

Run the example with:

```bash
python basic_usage.py
```

## Creating Your Own Examples

When using the SDK in your own projects, you'll typically:

1. Install the package: `pip install meltingface`
2. Import the Prompt class: `from meltingface.prompt import Prompt`
3. Load prompts: `prompt = Prompt.from_hub("username/prompt-name")`
4. Use the prompt text in your application

For private prompts, you can either:
- Pass your API key directly: `Prompt.from_hub("username/prompt-name", api_key="your-api-key")`
- Set the `MELTINGFACE_API_KEY` environment variable 