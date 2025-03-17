from unittest.mock import patch
from meltingface.prompt import Prompt

def test_prompt_init():
    p = Prompt(text="Hello", repo_id="owner/repo", version="v1", metadata={"k": "v"})
    assert p.text == "Hello"
    assert p.repo_id == "owner/repo"
    assert p.version == "v1"
    assert p.metadata == {"k": "v"}

@patch("meltingface.hub.from_hub")  # <-- patch the actual function in hub.py
def test_prompt_from_hub(mock_from_hub):
    """
    Test that Prompt.from_hub calls the underlying hub.from_hub function
    with the correct arguments.
    """
    mock_from_hub.return_value = "MOCKED_PROMPT"

    prompt = Prompt.from_hub(
        "owner/repo",
        version="v2",
        cache_dir="/tmp/cache",
        force_download=True
    )

    # Ensure hub.from_hub was called with the same args
    mock_from_hub.assert_called_once_with(
        repo_id="owner/repo",
        version="v2",
        cache_dir="/tmp/cache",
        force_download=True
    )

    # The result is the mock return value
    assert prompt == "MOCKED_PROMPT"
