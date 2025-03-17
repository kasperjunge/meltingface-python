import os
import json

def get_cache_dir():
    """
    Return the default cache directory, e.g. ~/.meltingface/prompts
    """
    home = os.path.expanduser("~")
    cache_dir = os.path.join(home, ".meltingface", "prompts")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def _get_cache_file(repo_id: str, version: str, cache_dir: str) -> str:
    """
    Build a cache file path like: ~/.meltingface/prompts/owner-repo-version.json
    If version=None, treat it as 'latest' in the file name.
    """
    version_str = version or "latest"
    # Convert e.g. "owner/repo" => "owner-repo"
    safe_repo_id = repo_id.replace("/", "-")
    filename = f"{safe_repo_id}-{version_str}.json"
    return os.path.join(cache_dir, filename)

def prompt_in_cache(repo_id: str, version: str, cache_dir: str) -> bool:
    """
    Check if the prompt file exists on disk.
    """
    return os.path.isfile(_get_cache_file(repo_id, version, cache_dir))

def load_cached_prompt(repo_id: str, version: str, cache_dir: str):
    from .prompt import Prompt  # to avoid circular import

    path = _get_cache_file(repo_id, version, cache_dir)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Prompt(
        text=data["text"],
        repo_id=data["repo_id"],
        version=data["version"],
        metadata=data.get("metadata", {})
    )

def cache_prompt(prompt, cache_dir):
    path = _get_cache_file(prompt.repo_id, prompt.version, cache_dir)
    data = {
        "text": prompt.text,
        "repo_id": prompt.repo_id,
        "version": prompt.version,
        "metadata": prompt.metadata
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
