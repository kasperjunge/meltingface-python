from meltingface.utils import (
    _get_cache_file,
    prompt_in_cache,
    load_cached_prompt,
    cache_prompt
)
from meltingface.prompt import Prompt

def test__get_cache_file():
    repo_id = "owner/repo"
    version = "v1"
    cache_dir = "/some/cache/dir"
    path = _get_cache_file(repo_id, version, cache_dir)
    # Should produce /some/cache/dir/owner-repo-v1.json
    assert path == "/some/cache/dir/owner-repo-v1.json"

def test__get_cache_file_latest():
    # version=None => "latest"
    repo_id = "owner/repo"
    version = None
    cache_dir = "/some/cache/dir"
    path = _get_cache_file(repo_id, version, cache_dir)
    assert path == "/some/cache/dir/owner-repo-latest.json"

def test_prompt_in_cache(temp_cache_dir):
    # Initially, there's no file => not in cache
    assert not prompt_in_cache("owner/repo", "v1", temp_cache_dir)

    # Create the file and check again
    file_path = _get_cache_file("owner/repo", "v1", temp_cache_dir)
    with open(file_path, "w") as f:
        f.write("{}")

    assert prompt_in_cache("owner/repo", "v1", temp_cache_dir)

def test_cache_and_load_prompt(temp_cache_dir):
    prompt = Prompt(text="Hello world", repo_id="owner/repo", version="v1", metadata={"foo": "bar"})
    cache_prompt(prompt, temp_cache_dir)

    # Now we load it back
    loaded = load_cached_prompt("owner/repo", "v1", temp_cache_dir)
    assert loaded.text == "Hello world"
    assert loaded.repo_id == "owner/repo"
    assert loaded.version == "v1"
    assert loaded.metadata == {"foo": "bar"}
