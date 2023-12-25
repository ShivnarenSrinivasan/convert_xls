import enum
import io
import pandas as pd
import warnings


class FileType(enum.StrEnum):
    """Conversion file types."""

    XLS = 'xls'
    CSV = 'csv'


def convert(from_: FileType, to: FileType, content: bytes) -> io.StringIO | io.BytesIO:
    """Return converted content."""
    func = _CONVERSION_MAPPING[(from_, to)]
    return func(content)


def _to_xls_content(csv: bytes) -> io.BytesIO:
    """Return xls represention of data."""
    df = pd.read_csv(io.BytesIO(csv))
    buffer = io.BytesIO()

    def _write():
        with pd.ExcelWriter(buffer, engine='xlwt') as writer:
            df.to_excel(writer, index=False)

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        _write()

    return io.BytesIO(buffer.getvalue())


def _from_xls(xls: bytes) -> io.StringIO:
    """Return csv represention of xls bytes."""
    df = pd.read_excel(io.BytesIO(xls))

    return io.StringIO(df.to_csv(index=False))


_CONVERSION_MAPPING = {
    (FileType.CSV, FileType.XLS): _to_xls_content,
    (FileType.XLS, FileType.CSV): _from_xls,
}
