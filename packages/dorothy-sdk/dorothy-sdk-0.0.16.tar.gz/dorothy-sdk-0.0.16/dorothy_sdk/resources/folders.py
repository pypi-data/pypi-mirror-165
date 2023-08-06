from requests import Session
from dorothy_sdk.utils import url_join


class CrossValidationFolders:
    resource = "cross_validation/cluster/"
    dataset: str = None
    cluster_id: str = None
    file_url: str = None

    def __init__(self, session: Session, host: str, **kwargs):
        self._session: Session = session
        self._service_host = host
        if kwargs.get("dataset"):
            self.dataset = kwargs.get("dataset")
        if kwargs.get("cluster_id"):
            self.cluster_id = kwargs.get("cluster_id")

    def get(self, cluster_id: str = None, dataset: str = None):
        search_parameter = {}
        if cluster_id or self.cluster_id:
            search_parameter.update({"cluster_id": cluster_id or self.cluster_id})
        if dataset or self.dataset:
            search_parameter.update({"dataset": dataset or self.dataset})
        response = self._session.get(url_join(self._service_host, self.resource), params=search_parameter)
        if response.status_code == 200:
            body = response.json()
            if not isinstance(body, dict) and (self.cluster_id or cluster_id):
                body = [element for element in body if element.get("cluster_id") == self.cluster_id][0]
            self.file_url = body.get("file_url")
            if cluster_id and not self.cluster_id:
                self.cluster_id = cluster_id
            if dataset and not self.dataset:
                self.dataset = dataset
            return body
        elif response.status_code == 404:
            raise ValueError("There are no folders for this dataset or cluster id not found.")
        else:
            response.raise_for_status()

    def download_file(self, path: str = None):
        if not self.file_url and not self.cluster_id:
            raise ValueError("Cluster id is mandatory to download file")
        if not self.file_url and self.cluster_id:
            self.get()
        if self.file_url:
            request = self._session.get(self.file_url)
            request.raise_for_status()
            if request.status_code == 200:
                if path:
                    with open(path, mode="r+") as file:
                        file.write(request.content)
                    return
                return request.content
            else:
                raise RuntimeError("Could not download image")
