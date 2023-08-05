from typing import TYPE_CHECKING

from ._search_data_provider import FilingsSearchData
from .._content_type import ContentType
from ...delivery._data._data_provider import DataProviderLayer, BaseResponse

if TYPE_CHECKING:
    from ...content._types import OptDict

from ...delivery._data._endpoint_data import RequestMethod


class Definition(DataProviderLayer[BaseResponse[FilingsSearchData]]):
    """
    This class provide searching and filtering for Filings documents
    Query string can be built by using data-store endpoint in API playgound

    Parameters
    ----------
    query: str
        Full query string to request the search. This will override other parameters.
    variables: dict
        Variables can be used for this query

    Examples
    --------
    >>> from refinitiv.data.content import filings
    >>> query = '{  FinancialFiling(filter: {AND: [{FilingDocument: {DocumentSummary: {FeedName: {EQ: "Edgar"}}}}, {FilingDocument: {DocumentSummary: {FormType: {EQ: "10-Q"}}}}, {FilingDocument: {DocumentSummary: {FilingDate: {BETWN: {FROM: "2020-01-01T00:00:00Z", TO: "2020-12-31T00:00:00Z"}}}}}]}, sort: {FilingDocument: {DocumentSummary: {FilingDate: DESC}}}, limit: 10) {    _metadata {      totalCount    }    FilingDocument {      Identifiers {        Dcn      }      DocId      FinancialFilingId      DocumentSummary {        DocumentTitle        FeedName        FormType        HighLevelCategory        MidLevelCategory        FilingDate        SecAccessionNumber        SizeInBytes          }  FilesMetaData {        FileName        MimeType      }    }  }}'
    >>> definition = filings.search.Definition(query=query)
    >>> response = definition.get_data()
    >>> # response.data.df for prioritize information
    >>> # response.data.raw to see all data responded from the service
    >>> response.data.files[0].download(path="C:\\Downloads\\download_test")
    >>> # To download all files from search
    >>> response.data.files.download()

    >>> # async download files
    >>> await response.data.files[0].download_async()
    >>> await response.data.files.download_async()
    """

    def __init__(self, query: str = None, variables: "OptDict" = None):
        self.query = query
        self.variables = variables

        super().__init__(
            ContentType.FILINGS_SEARCH,
            method=RequestMethod.POST,
            query=self.query,
            variables=self.variables,
        )
