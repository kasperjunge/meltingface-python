#!/usr/bin/env python3
"""
Test that Prompt can be imported directly from meltingface
"""

try:
    from meltingface import Prompt
    print("✅ Successfully imported Prompt directly from meltingface!")
    print(f"Prompt class: {Prompt}")
    
    # Test that we can create a Prompt instance
    p = Prompt(text="Test prompt", repo_id="test/repo", version="1.0.0")
    print(f"Created prompt with text: {p.text}")
    
    # Make sure from_hub method is available
    print(f"from_hub method: {Prompt.from_hub}")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    
except Exception as e:
    print(f"❌ Error: {e}") 