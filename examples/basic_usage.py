#!/usr/bin/env python3
"""
Basic example of using the MeltingFace SDK

This example demonstrates how to:
1. Import the Prompt class
2. Load a prompt from the MeltingFace hub
3. Access prompt text and metadata
"""

from meltingface import Prompt

# Load a prompt from the hub
# For private prompts, you can use:
# prompt = Prompt.from_hub("kasperjuunge/clarification-step", api_key="your-api-key")
# Or set the MELTINGFACE_API_KEY environment variable
prompt = Prompt.from_hub("kasperjuunge/clarification-step")

# Print basic information
print(f"Loaded prompt: {prompt.repo_id}")
print(f"Version: {prompt.version}")
print("\nPrompt text:")
print("-" * 40)
print(prompt.text)
print("-" * 40)

# Access metadata
if prompt.metadata:
    print("\nMetadata:")
    print(f"Name: {prompt.metadata.get('name', 'N/A')}")
    print(f"Description: {prompt.metadata.get('description', 'N/A')}")
    print(f"Created: {prompt.metadata.get('created_at', 'N/A')}")
    print(f"Public: {'Yes' if prompt.metadata.get('is_public', False) else 'No'}")
    
    if prompt.metadata.get('user'):
        print(f"Author: {prompt.metadata['user'].get('name')} (@{prompt.metadata['user'].get('username')})") 