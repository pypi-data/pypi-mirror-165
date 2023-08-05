import pandas as pd
from typing import Callable

from .._content_provider import (
    UniverseContentValidator,
    ErrorParser,
)

from ...delivery._data._data_provider import (
    DataProvider,
    RequestFactory,
    ResponseFactory,
    Data,
)
from .retrieval import Definition as RetrievalDefinition
from ._retrieval_data_provider import (
    ListOfFile,
    DownloadFileError,
    DownloadAllFileResponse,
)


class FilingsSearchRequestFactory(RequestFactory):
    def get_body_parameters(self, *_, **kwargs) -> dict:
        query = kwargs.get("query", "")
        variables = kwargs.get("variables", {})
        return {"query": query, "variables": variables}


class FilingsSearchFile:
    def __init__(
        self,
        title: str = None,
        filename: str = None,
        mimetype: str = None,
        dcn: str = None,
        doc_id: str = None,
        filing_id: int = None,
    ):
        """
        Parameters
        ----------
        title : str
            Document title of the file
        filename : str
            Name of the file
        mimetype : str
            Mime type of the file
        dcn: str
            DCN of the file
        doc_id: str
            Doc ID of the file
        filing_id: int
            Financial Filing ID
        """
        self.filename = filename
        self.title = title
        self.mimetype = mimetype
        self.dcn = dcn
        self.doc_id = doc_id
        self.filing_id = filing_id

    def _download_file(self):
        response = None
        error = False
        if pd.notna(self.filename) and self.filename:
            response = RetrievalDefinition(filename=self.filename).get_data()
        elif pd.notna(self.dcn) and self.dcn:
            response = RetrievalDefinition(dcn=self.dcn).get_data()
        elif pd.notna(self.doc_id) and self.doc_id:
            response = RetrievalDefinition(doc_id=self.doc_id).get_data()
        elif pd.notna(self.filing_id) and self.filing_id:
            response = RetrievalDefinition(filing_id=str(self.filing_id)).get_data()
        else:
            error = True
        return response, error

    def download(self, path: str = None) -> DownloadAllFileResponse:
        """

        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.

        Returns
        -------
        DownloadAllFileResponse
        """
        response, err = self._download_file()
        if err:
            raise DownloadFileError(
                code=None,
                message=f"Cannot download file. Missing one of Filename, DCN, DocID and Filing ID",
            )
        return response.data.files.download(path=path)

    async def download_async(
        self, path: str = None, callback: Callable = None
    ) -> DownloadAllFileResponse:
        """

        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.
        callback: Callable
            Callback function will be called after the process is completed

        Returns
        -------
        DownloadAllFileResponse
        """
        response, err = self._download_file()
        if err:
            errors = [
                DownloadFileError(
                    code=None,
                    message=f"Cannot download file. Missing one of Filename, DCN, DocID and Filing ID",
                )
            ]
            return DownloadAllFileResponse(files=[self], errors=errors)
        return await response.data.files.download_async(path=path, callback=callback)


class FilingsSearchData(Data):
    def __init__(self, raw, *args, **kwargs) -> None:
        super().__init__(raw=raw, *args, **kwargs)
        self._files = None

    def _get_data_df(self):
        data_df = []
        for row in self._raw["data"].get("FinancialFiling"):
            filing_document = row.get("FilingDocument", {})
            identifiers = filing_document.get("Identifiers", [])
            dcn = ""
            if len(identifiers) > 0:
                dcn = identifiers[0].get("Dcn", "")
            doc_id = filing_document.get("DocId", "")
            financial_filing_id = filing_document.get("FinancialFilingId", "")
            document_title = filing_document.get("DocumentSummary", {}).get(
                "DocumentTitle"
            )
            filenames = []
            if filing_document.get("FilesMetaData"):
                filenames = filing_document.get("FilesMetaData", {})
            if len(filenames) == 0:
                data_df.append(
                    [
                        document_title,
                        None,
                        None,
                        dcn,
                        doc_id,
                        financial_filing_id,
                    ]
                )
            for filename in filenames:
                data_df.append(
                    [
                        document_title,
                        filename.get("FileName"),
                        filename.get("MimeType"),
                        dcn,
                        doc_id,
                        financial_filing_id,
                    ]
                )
        return data_df

    @property
    def df(self):
        if self._dataframe is None and self._raw and "errors" not in self._raw:
            # generate headers for df
            headers = [
                {"title": "DocumentTitle", "type": "string"},
                {"title": "Filename", "type": "string"},
                {"title": "MimeType", "type": "string"},
                {"title": "Dcn", "type": "string"},
                {"title": "DocId", "type": "string"},
                {"title": "FinancialFilingId", "type": "int"},
            ]
            data_df = []
            if self._raw.get("data") is not None:
                data_df = self._get_data_df()
            data_df = {"headers": headers, "data": data_df}
            self._dataframe = self._dfbuilder(data_df, **self._kwargs)
        return self._dataframe

    @property
    def files(self):
        """
        Returns
        -------
        ListOfFile[FilingsSearchFile]
        """
        if self._files is None:
            self._files = ListOfFile()
            if self.df is not None and not self.df.empty:
                self._files.extend(FilingsSearchFile(*row) for row in self.df.values)
        return self._files


class FilingsSearchValidator(UniverseContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = super().validate(data)
        if not is_valid:
            return is_valid

        if data.get("content_data", {}).get("errors"):
            is_valid = False
            data["error_code"] = None
            data["error_message"] = data["content_data"]["errors"][0].get("message")

        return is_valid


filings_search_data_provider = DataProvider(
    request=FilingsSearchRequestFactory(),
    response=ResponseFactory(data_class=FilingsSearchData),
    validator=FilingsSearchValidator(),
    parser=ErrorParser(),
)
