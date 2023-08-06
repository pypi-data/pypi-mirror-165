import os
from typing import Optional, TypeVar
import tempfile
from pathlib import Path
from shutil import make_archive


import requests
from pydantic import BaseModel

from zenodo_rest.entities.deposition_file import DepositionFile
from zenodo_rest.entities.metadata import Metadata
from zenodo_rest.entities.bucket_file import BucketFile
from zenodo_rest import exceptions
from zenodo_rest.retries import retry_on_http_error

T = TypeVar("Deposition")


class Deposition(BaseModel):
    created: str
    doi: Optional[str]
    doi_url: Optional[str]
    files: Optional[list[DepositionFile]]
    id: str
    links: dict
    metadata: Metadata
    modified: str
    owner: int
    record_id: int
    record_url: Optional[str]
    state: str
    submitted: bool
    title: str

    @staticmethod
    def create(
        metadata: Metadata = None,
        prereserve_doi: Optional[bool] = None,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> T:
        """Create a deposition on the server, but do not publish it.

        :param metadata: The metadata to be used when creating the deposition.
            (defaults to an empty Metadata object with placeholders in required fields)
        :type metadata: Metadata
        :param prereserve_doi: Whether to prereserve a DOI or not, Zenodo seems to do it always, but documented this.
        :type prereserve_doi: Optional[bool]
        :param token: Your zenodo token
        :type token: Optional[str]
        :param base_url: The url for the target zenodo server
        :type base_url: Optional[str]
        :return: The Deposition object created (now containing server side created properties)
        :rtype: Deposition
        """

        if metadata is None:
            metadata = Metadata()
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")

        if prereserve_doi is True:
            metadata.prereserve_doi = True

        header = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{base_url}/api/deposit/depositions",
            json={"metadata": metadata.dict(exclude_none=True)},
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    @staticmethod
    @retry_on_http_error(codes_to_retry=[504])
    def retrieve(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> T:
        """Fetch a deposition by id from the remote

        :param deposition_id:
        :type deposition_id: str
        :param token: Your zenodo token
        :type token: Optional[str]
        :param base_url: The url for the target zenodo server
        :type base_url: Optional[str]
        :return: The deposition fetched by the remote
        :rtype: Deposition
        """

        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.get(
            f"{base_url}/api/deposit/depositions/{deposition_id}",
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def refresh(self, token: Optional[str] = None) -> T:
        """Refresh this deposition

        :param token: Your zenodo token
        :type token: Optional[str]
        :return: Refreshes this deposition from the remote
        :rtype: Deposition
        """

        return Deposition.retrieve(self.id, token)

    def get_latest(self, token: Optional[str] = None) -> T:
        """Gets the latest published version of this deposition

        :param token: Your zenodo token
        :type token: Optional[str]
        :return: The latest  version of this deposition.
        :rtype: Deposition
        """

        deposition: Deposition = self.refresh(token)
        latest_url = deposition.links.get("latest", None)
        if latest_url is None:
            return deposition
        latest_id = latest_url.rsplit("/", 1)[1]
        return Deposition.retrieve(latest_id, token)

    def get_latest_draft(self, token: Optional[str] = None) -> T:
        """Retrieve the latest draft related to this deposition

        :param token: Your zenodo token
        :type token: Optional[str]
        :return: The latest draft related to this deposition, or a NoDraftFound exception.
        :rtype: Deposition
        """

        deposition: Deposition = self.refresh(token)
        latest_draft_url = deposition.links.get("latest_draft", None)
        if latest_draft_url is None:
            raise exceptions.NoDraftFound(deposition.id)

        if token is None:
            token = os.getenv("ZENODO_TOKEN")

        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(
            latest_draft_url,
            headers=header,
        )
        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def get_bucket(self) -> str:
        return self.links.get("bucket")

    @retry_on_http_error(codes_to_retry=[502])
    def upload_file(self, path_or_file: str, token: Optional[str] = None) -> BucketFile:
        """Upload or overwrite a file or path attachment for a deposition

        :param path_or_file: A path to zip and upload or a file_path to upload
        :type path_or_file: str
        :param token: Your zenodo token
        :type token: Optional[str]
        :return: The object for a successfully uploaded file
        :rtype: BucketFile
        """

        bucket_url = self.get_bucket()
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        path = Path(path_or_file)
        tempdir = None
        if path.is_dir():
            tempdir = tempfile.TemporaryDirectory()
            zip_file = os.path.join(tempdir.name, path.stem)
            make_archive(zip_file, "zip", root_dir=path.absolute())
            path = Path(f"{zip_file}.zip")

        header = {"Authorization": f"Bearer {token}"}
        with open(path.absolute(), "rb") as fp:
            r = requests.put(
                f"{bucket_url}/{path.name}",
                data=fp,
                headers=header,
            )

        if tempdir is not None:
            tempdir.cleanup()
        r.raise_for_status()
        return BucketFile.parse_obj(r.json())

    def delete_file(
        self, file_id: str, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> int:
        """Delete a file from this deposition if it is not yet published

        :param file_id: The id of the file to be deleted, which is stored in this deposition's bucket.
        :type  file_id: str
        :param token: Your zenodo token
        :type token: Optional[str]
            (defaults to ZENODO_TOKEN envvar)
        :param base_url: The base url of the zenodo server
            (defaults to ZENODO_URL envvar)
        :type base_url: Optional[str]
        :return: The HTTP response code of the deletion request.
        :rtype: int
        """

        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.delete(
            f"{base_url}/api/deposit/depositions/{self.id}/files/{file_id}",
            headers=header,
        )

        response.raise_for_status()
        return response.status_code

    def delete_files(
        self, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> list[int]:
        """Delete all files from this deposition if it is not yet published

        :param token: Your zenodo token
        :type token: Optional[str]
            (defaults to ZENODO_TOKEN envvar)
        :param base_url: The base url of the zenodo server
            (defaults to ZENODO_URL envvar)
        :type base_url: Optional[str]
        :return: A list of the HTTP response codes of the file deletion requests
        :rtype: list[int]
        """

        return [self.delete_file(file.id, token, base_url) for file in self.files]
