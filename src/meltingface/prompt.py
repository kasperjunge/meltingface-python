class Prompt:
    def __init__(self, text: str, repo_id: str, version: str = None, metadata: dict = None):
        """
        A simple Prompt object.

        Args:
            text (str): The main prompt string.
            repo_id (str): The MeltingFace repository identifier (e.g. 'owner/name').
            version (str): Optional version of the prompt. Defaults to None (latest).
            metadata (dict): Optional dictionary with extra information about the prompt.
        """
        self.text = text
        self.repo_id = repo_id
        self.version = version
        self.metadata = metadata or {}

    @classmethod
    def from_hub(cls, repo_id: str, version: str = None, cache_dir: str = None, force_download: bool = False):
        """
        Create a Prompt by fetching from MeltingFace hub.

        Args:
            repo_id (str): The 'owner/repo' identifier.
            version (str): The version of the prompt. Defaults to None (which means 'latest').
            cache_dir (str): Optional path to store (and retrieve) cached prompts.
            force_download (bool): If True, re-download even if a cached version is found.

        Returns:
            Prompt: The loaded prompt instance.
        """
        from .hub import from_hub  # to avoid circular imports
        return from_hub(
            repo_id=repo_id,
            version=version,
            cache_dir=cache_dir,
            force_download=force_download
        )
