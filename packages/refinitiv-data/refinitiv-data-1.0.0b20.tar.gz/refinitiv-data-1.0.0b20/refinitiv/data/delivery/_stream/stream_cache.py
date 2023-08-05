# coding: utf8


class StreamCacheIterator:
    """StreamCache Iterator class"""

    def __init__(self, stream_cache):
        if stream_cache.get_fields():
            self._field_values = list(stream_cache.get_fields().items())
        else:
            self._field_values = []
        self._index = 0

    def __next__(self):
        """Return the next field value from stream cache"""
        if self._index < len(self._field_values):
            result = self._field_values[self._index]
            self._index += 1
            return result
        raise StopIteration()


class StreamCache:
    """
    StreamCache contains all retrieved data from stream subscription.

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error
    """

    def __init__(self, name, fields=None, service=None, status=None, record=None):
        self._name = name
        self._fields = fields if fields else []
        self._service = service
        self._status = status
        self._record = record

    ###################################################
    #  Access to StreamCache as a dict                #
    ###################################################

    def keys(self):
        if self._record and self._record.get("Fields"):
            return self._record["Fields"].keys()
        return {}.keys()

    def values(self):
        if self._record and self._record.get("Fields"):
            return self._record["Fields"].values()
        return {}.values()

    def items(self):
        if self._record and self._record.get("Fields"):
            return self._record["Fields"].items()
        return {}.items()

    ###################################################
    #  Make StreamCache iterable                      #
    ###################################################

    def __iter__(self):
        return StreamCacheIterator(self)

    def __getitem__(self, field):
        if (
            self._record
            and self._record.get("Fields")
            and field in self._record["Fields"].keys()
        ):
            return self._record["Fields"][field]
        raise KeyError(f"Field '{field}' not in Stream cache")

    def __len__(self):
        return len(self._fields)

    def __repr__(self):
        rep = str(
            {
                "name": self.name,
                "service": self.service,
                "fields": dict(list(self.items())),
            }
        )
        return rep

    def __str__(self):
        if self.service:
            return str(
                "|".join([self.service, self.name])
                + "["
                + ",".join([f"{f}:{v}" for f, v in self.items()])
                + "]"
            )
        else:
            return str(
                "|".join(["Unknown service", self.name])
                + "["
                + ",".join([f"{f}:{v}" for f, v in self.items()])
                + "]"
            )

    ###################################################
    #  StreamCache properties                         #
    ###################################################

    @property
    def name(self):
        return self._name

    @property
    def service(self):
        return self._service

    @property
    def fields(self):
        if self._record and self._record.get("Fields"):
            return self._record["Fields"].keys()
        return None

    @property
    def status(self):
        return self._status

    @property
    def is_ok(self):
        return True if self._status.get("Data") == "Ok" else False

    # ###################################################
    # #  StreamingCache data accessors                  #
    # ###################################################

    def get_field_value(self, field):
        if (
            self._record
            and self._record.get("Fields")
            and field in self._record["Fields"].keys()
        ):
            return self._record["Fields"][field]

    def get_fields(self, fields=None) -> dict:
        if not self._record:
            return dict.fromkeys(fields or self._fields)

        if not fields:
            return self._record.get("Fields")

        return {**dict.fromkeys(fields), **self._record.get("Fields")}
