import os
import requests
from .prompt import Prompt
from .utils import (
    get_cache_dir,
    prompt_in_cache,
    load_cached_prompt,
    cache_prompt
)

# Update to the deployed API URL
MELTINGFACE_API_BASE = "https://api.meltingface.eu/api/v1"
MELTINGFACE_API_KEY_ENV = "MELTINGFACE_API_KEY"

def from_hub(repo_id, version=None, cache_dir=None, force_download=False, api_key=None):
    """
    Internal function called by Prompt.from_hub().
    """
    owner, repo_name = parse_repo_id(repo_id)
    if cache_dir is None:
        cache_dir = get_cache_dir()  # default to ~/.meltingface/prompts

    # 1) Check local cache
    if not force_download and prompt_in_cache(repo_id, version, cache_dir):
        return load_cached_prompt(repo_id, version, cache_dir)

    # 2) Construct the request
    url = f"{MELTINGFACE_API_BASE}/prompts/{owner}/{repo_name}"
    params = {}
    if version:
        params["version"] = version

    # Use API key from param or environment variable for private prompts
    headers = {}
    if api_key:
        headers["X-MeltingFace-API-Key"] = api_key
    elif os.environ.get(MELTINGFACE_API_KEY_ENV):
        headers["X-MeltingFace-API-Key"] = os.environ[MELTINGFACE_API_KEY_ENV]

    response = requests.get(url, params=params, headers=headers)
    # 3) Basic error handling
    if response.status_code == 404:
        raise ValueError(f"Prompt not found for repo_id={repo_id}, version={version}")
    elif response.status_code == 401 or response.status_code == 403:
        raise ValueError(f"Authentication error: This may be a private prompt that requires an API key.")
    response.raise_for_status()

    data = response.json()
    # Expecting something like: { "text": "...", "metadata": {...}, "version": "some_version_or_latest" }

    text = data["text"]
    metadata = data.get("metadata", {})
    actual_version = data.get("version", version)  # fallback to user-supplied or "latest"

    # Create the Prompt
    prompt = Prompt(text=text, repo_id=repo_id, version=actual_version, metadata=metadata)

    # 4) Cache it
    cache_prompt(prompt, cache_dir)

    return prompt

def parse_repo_id(repo_id: str):
    """
    Splits 'owner/repo' into ('owner', 'repo').
    Could add validations, etc.
    """
    if "/" not in repo_id:
        raise ValueError("repo_id must be in the format 'owner/repo'")
    owner, repo = repo_id.split("/", 1)
    return owner, repo
