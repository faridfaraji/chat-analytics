

from typing import List, Any
import tiktoken
import json

from chat_analytics.core.exceptions import ArtifactTooLargeError

TOKEN_LIMIT = 15000


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens


def get_artifacts(artifact_ids: List[str], query: Any):
    queriable_ids = []
    artifacts_string = ""
    for artifact_id in artifact_ids:
        artifact = json.dumps(query(artifact_id))
        if num_tokens_from_string(artifacts_string + artifact, "cl100k_base") < TOKEN_LIMIT:
            artifacts_string += artifact
            queriable_ids.append(artifact_id)
    return queriable_ids


def get_artifact_size_confirmation(artifact_id: str, query: Any):
    artifact = json.dumps(query(artifact_id))
    if num_tokens_from_string(artifact, "cl100k_base") < TOKEN_LIMIT:
        return True
    raise ArtifactTooLargeError
