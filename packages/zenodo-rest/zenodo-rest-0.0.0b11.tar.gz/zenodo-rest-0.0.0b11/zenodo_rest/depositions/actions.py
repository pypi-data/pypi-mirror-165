import os
from typing import Optional
import logging

import requests

from zenodo_rest.entities.deposition import Deposition
from zenodo_rest.entities.metadata import Metadata

logging.basicConfig()
logger = logging.getLogger()


def update_metadata(
    deposition_id: str,
    metadata: Metadata,
    token: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Deposition:
    """Update the metadata of a not yet published deposition

    :param deposition_id: The id of the deposition to update
    :type deposition_id: str
    :param metadata: The metadata to update the deposition with
    :type metadata: Metadata
    :param token: Your zenodo token
        (defaults to the ZENODO_TOKEN envvar)
    :type token: Optional[str]
    :param base_url: The url to the target zenodo server
    :type base_url: Optional[str]
    :return: The deposition with updated metadata
    :rtype: Deposition
    """

    if token is None:
        token = os.getenv("ZENODO_TOKEN")
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    response = requests.put(
        f"{base_url}/api/deposit/depositions/{deposition_id}",
        json={"metadata": metadata.dict(exclude_none=True)},
        headers=header,
    )

    response.raise_for_status()
    return Deposition.parse_obj(response.json())


def delete_remote(
    deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
) -> requests.Response:
    """Delete a not yet published draft of a deposition

    :param deposition_id: The id of the depsition to be deleted
    :type deposition_id: str
    :param token: Your zenodo token
        (defaults to the ZENODO_TOKEN envvar)
    :type token: Optional[str]
    :param base_url: The url to the target zenodo server
    :type base_url: Optional[str]
    :return: The requests HTTP response
    :rtype: requests.Response
    """

    if token is None:
        token = os.getenv("ZENODO_TOKEN")
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.delete(
        f"{base_url}/api/deposit/depositions/{deposition_id}",
        headers=header,
    )

    response.raise_for_status()
    return response


def publish(
    deposition_id: str,
    token: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Deposition:
    """Publish a deposition

    :param deposition_id: The id of the deposition to be published
    :type deposition_id: str
    :param token: Your zenodo token
        (defaults to the ZENODO_TOKEN envvar)
    :type token: Optional[str]
    :param base_url: The url to the target zenodo server
    :type base_url: Optional[str]
    :return: The published deposition
    :rtype: Deposition
    """

    if token is None:
        token = os.getenv("ZENODO_TOKEN")
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{base_url}/api/deposit/depositions/{deposition_id}/actions/publish",
        headers=header,
    )

    response.raise_for_status()
    return Deposition.parse_obj(response.json())


def new_version(
    deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
) -> Deposition:
    """Create a new version draft of a deposition

    Only one draft may exist at a time, this may fail when a draft already exists

    :param deposition_id: The id of the deposition to create a new version of.
    :type deposition_id: str
    :param token: Your zenodo token
        (defaults to the ZENODO_TOKEN envvar)
    :type token: Optional[str]
    :param base_url: The url to the target zenodo server
    :type base_url: Optional[str]
    :return: The currently published deposition (now containing a link to the draft)
    :rtype: Deposition
    """

    if token is None:
        token = os.getenv("ZENODO_TOKEN", token)
    if base_url is None:
        base_url = os.getenv("ZENODO_URL")
    header = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{base_url}/api/deposit/depositions/{deposition_id}/actions/newversion",
        headers=header,
    )

    response.raise_for_status()
    deposition: Deposition = Deposition.parse_obj(response.json())
    return deposition


def search(
    query: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    page: Optional[str] = None,
    size: Optional[int] = None,
    all_versions: Optional[bool] = None,
    token: Optional[str] = None,
) -> list[Deposition]:
    """Search for depositions

    :param query: An elasticsearch formatted query
    :type query: Optional[str]
    :param status: Filter by publication status; either 'result' or 'published'
    :type status: Optional[str]
    :param sort: Sort order 'bestmatch' or 'mostrecent' prefix with - to sort descending.
    :type sort: Optional[str]
    :param page: The page of the search to return
    :type page: Optional[str]
    :param size: The size limit per page
    :type size: Optional[str]
    :param all_versions: 'true' to show all versions, 'false' to hide other versions
    :type all_versions: Optional[str]
    :param token: your zenodo token
    :return: The list of depositions found
    :rtype: list[Deposition]
    """

    if token is None:
        token = os.getenv("ZENODO_TOKEN")

    base_url = os.getenv("ZENODO_URL")
    header = {"Authorization": f"Bearer {token}"}
    params: dict = {}
    if query is not None:
        params["q"] = query
    if status is not None:
        params["status"] = status
    if sort is not None:
        params["sort"] = sort
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if all_versions:
        params["all_versions"] = "true"
    response = requests.get(
        f"{base_url}/api/deposit/depositions", headers=header, params=params
    )

    response.raise_for_status()
    return [Deposition.parse_obj(x) for x in response.json()]
