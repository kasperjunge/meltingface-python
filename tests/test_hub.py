import pytest
from unittest.mock import patch, MagicMock

from meltingface.hub import from_hub, parse_repo_id
from meltingface import Prompt
from meltingface.utils import _get_cache_file

def test_parse_repo_id_valid():
    owner, repo = parse_repo_id("someowner/somerepo")
    assert owner == "someowner"
    assert repo == "somerepo"

def test_parse_repo_id_invalid():
    with pytest.raises(ValueError) as exc_info:
        parse_repo_id("no_slash")
    assert "repo_id must be in the format" in str(exc_info.value)

@patch("meltingface.hub.requests.get")
def test_from_hub_success(mock_get, temp_cache_dir):
    # Mock the requests response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "text": "mock text",
        "metadata": {"author": "test"},
        "version": "mock_version"
    }
    mock_get.return_value = mock_response

    # from_hub call
    prompt = from_hub("someowner/somerepo", version="v1", cache_dir=temp_cache_dir, force_download=True)

    # Check that the request was made with the correct URL and params
    mock_get.assert_called_once_with(
        "https://meltingface.eu/api/prompts/someowner/somerepo",
        params={"version": "v1"}
    )

    # Verify the returned prompt
    assert isinstance(prompt, Prompt)
    assert prompt.text == "mock text"
    assert prompt.repo_id == "someowner/somerepo"
    assert prompt.version == "mock_version"
    assert prompt.metadata == {"author": "test"}

    # Check that it was cached (file should exist with the data)
    path = _get_cache_file("someowner/somerepo", "mock_version", temp_cache_dir)
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    assert '"text": "mock text"' in data

@patch("meltingface.hub.requests.get")
def test_from_hub_not_found(mock_get, temp_cache_dir):
    # Mock a 404 response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError) as exc_info:
        from_hub("owner/repo", version="v1", cache_dir=temp_cache_dir, force_download=True)
    assert "Prompt not found" in str(exc_info.value)

@patch("meltingface.hub.requests.get")
@patch("meltingface.hub.load_cached_prompt", return_value=Prompt("cached text", "owner/repo", version="v1"))
@patch("meltingface.hub.prompt_in_cache", return_value=True)
def test_from_hub_uses_cache(
    mock_in_cache,    # for prompt_in_cache
    mock_load_cached, # for load_cached_prompt
    mock_get,         # for requests.get
    temp_cache_dir
):
    """
    If prompt_in_cache returns True and force_download=False,
    we shouldn't hit the network and should load from cache.
    """
    prompt = from_hub("owner/repo", version="v1", cache_dir=temp_cache_dir, force_download=False)

    # Because prompt_in_cache is True and force_download=False, requests.get not called
    mock_get.assert_not_called()

    # We expect load_cached_prompt to have returned a cached Prompt
    mock_load_cached.assert_called_once_with("owner/repo", "v1", temp_cache_dir)
    assert isinstance(prompt, Prompt)
    assert prompt.text == "cached text"
    assert prompt.repo_id == "owner/repo"
    assert prompt.version == "v1"

@patch("meltingface.hub.prompt_in_cache", return_value=False)
@patch("meltingface.hub.requests.get")
def test_from_hub_force_download_false_no_cache(
    mock_get,
    mock_in_cache,
    temp_cache_dir
):
    """
    If prompt_in_cache is False, from_hub should call requests.get,
    even if force_download=False.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "text": "some text",
        "metadata": {},
        "version": "v2"
    }
    mock_get.return_value = mock_response

    prompt = from_hub("owner/repo", version="v1", cache_dir=temp_cache_dir, force_download=False)

    # Because the cache was reported as empty, we do call requests.get
    mock_get.assert_called_once()
    assert isinstance(prompt, Prompt)
    assert prompt.text == "some text"
    assert prompt.version == "v2"
