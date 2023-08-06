from urllib.parse import urlsplit, urlunsplit, SplitResult


class BaseUrlConverter:
    """A :class:`BaseUrlConverter` instance is used to convert
    one URL to another. The base class is a pass-through implementation
    intended to have its private classes overridden in subclasses.
    """
    def convert(self, url: str):
        """ Returns a URL :type:`str` converted from another
        URL :type:`str`.

        :param url: the URL to be converted
        """
        parts = urlsplit(url)
        return urlunsplit(
            (
                self._convert_scheme(parts),
                self._convert_netloc(parts),
                self._convert_path(parts),
                self._convert_query(parts),
                self._convert_fragment(parts)
            )
        )

    def _convert_scheme(self, parts: SplitResult) -> str:
        return parts.scheme

    def _convert_netloc(self, parts: SplitResult) -> str:
        return parts.netloc

    def _convert_path(self, parts: SplitResult) -> str:
        return parts.path

    def _convert_query(self, parts: SplitResult) -> str:
        return parts.query

    def _convert_fragment(self, parts: SplitResult) -> str:
        return parts.fragment
