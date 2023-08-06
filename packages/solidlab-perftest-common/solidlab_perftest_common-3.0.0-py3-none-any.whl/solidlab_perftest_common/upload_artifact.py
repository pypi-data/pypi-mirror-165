import mimetypes
from typing import Tuple, Optional

from urllib3 import Timeout


def validate_artifact_endpoint(value: str) -> str:
    """
    Validates an artifact endpoint. Accepts multiple partial endpoints.
    Always returns a canonical value, ending in: /artifact/
    :param value: an artifact endpoint, optionally including the end /artifact/
    :return: a canonical value, ending in: /artifact/
    """
    # TODO use full regex to check if only allowed forms are given
    #        https?://.*/(experiment|perftest|testenv)/[0-9]+/?(artifact)?/?
    if not isinstance(value, str):
        raise ValueError(
            f"artifact_endpoint must be a URL (and thus a string and not {type(value)})"
        )
    if not value.startswith("https://") and not value.startswith("http://"):
        raise ValueError("artifact_endpoint must be a URL")
    if (
        "/perftest/" not in value
        and "/testenv/" not in value
        and "/experiment/" not in value
    ):
        raise ValueError(
            "artifact_endpoint must contain a full object endpoint "
            "(and thus contain /perftest/{id}/ /experiment/{id}/ or /testenv/{id}/)"
        )
    if not value.endswith("/"):
        value = value + "/"
    if (
        value.endswith("perftest/")
        or value.endswith("experiment/")
        or value.endswith("testenv/")
    ):
        raise ValueError(
            "artifact_endpoint must contain a full object endpoint "
            "(and thus contain /perftest/{id}/ /experiment/{id}/ or /testenv/{id}/)"
        )
    if not value.endswith("/artifact/"):
        value = value + "artifact/"
    return value


def upload_artifact_file(
    session,
    *,
    artifact_endpoint: str,
    attach_type: str,
    sub_type: str,
    description: str,
    filename: str,
    content_type: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> Tuple[int, str]:
    if not content_type:
        guesses = mimetypes.guess_type(filename)
        if not guesses:
            raise ValueError(f"mime type could not be guessed from filename.")
        content_type = guesses[0]
        # logger.debug(f"Guessed mime-type from filename: {mime_type!r}")

    with open(filename, "rb") as f:
        content = f.read()

        return upload_artifact(
            session,
            artifact_endpoint=artifact_endpoint,
            attach_type=attach_type,
            sub_type=sub_type,
            description=description,
            content=content,
            content_type=content_type,
            auth_token=auth_token,
        )


def upload_artifact(
    session,
    *,
    artifact_endpoint: str,
    attach_type: str,
    sub_type: str,
    description: str,
    content_type: str,
    content: bytes,
    auth_token: Optional[str] = None,
) -> Tuple[int, str]:
    """

    :param session:
    :param artifact_endpoint:
    :param attach_type:
    :param sub_type:
    :param description:
    :param content_type: examples "text/csv" "text/plain" "image/svg+xml" "image/png"
    :param content:
    :return:
    """
    artifact_endpoint = validate_artifact_endpoint(artifact_endpoint)

    headers = {
        "Content-Type": content_type,
        "X-Solidlab-Artifact-Type": attach_type,
        "X-Solidlab-Artifact-Subtype": sub_type,
        "X-Solidlab-Artifact-Description": description,
    }

    if auth_token:
        # Solidlab-Perftest-Auth is also supported
        headers["X-Solidlab-Perftest-Auth"] = auth_token

    post_attach_meta_resp = session.post(
        artifact_endpoint,
        params={},
        headers=headers,
        timeout=Timeout(connect=2.0, read=3.0),
        data=content,
    )
    post_attach_meta_resp.raise_for_status()
    artifact_url = post_attach_meta_resp.json()["@id"]
    artifact_id = post_attach_meta_resp.json()["id"]
    return artifact_id, artifact_url
