import csv
from typing import Generator, List, MutableMapping, Union

from tinytable.functional.features import column_names
from tinytable.functional.rows import itertuples
from tinytable.functional.utils import combine_names_rows, row_dicts_to_data



def convert_str(value: str) -> Union[float, int, bool, str]:
    """Takes a str value and tries to convert it to float, int, or bool
       Returns converted value if successful, or str value if fails to convert.
    """
    value = str(value)
    if value.count('.') == 1:
        try:
            return float(value)
        except ValueError:
            pass
    if value.isnumeric():
        try:
            return int(value)
        except ValueError:
            pass
    if value in {'True', 'False'}:
        return bool(value)
    return value


def chunk_csv_file(
    path: str,
    chunksize=5,
    newline='',
    encoding='utf-8-sig'
) -> Generator[dict, None, None]:
    """
    Read chunks of table object from given CSV file.
    """
    column_names = []
    rows = []
    first = True
    chunk_end = chunksize
    with open(path, 'r', newline=newline, encoding=encoding) as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        for i, row in enumerate(csv.reader(f, dialect)):
            if first:
                column_names = row
                first = False
            else:
                rows.append([convert_str(v) for v in row])
            if i == chunk_end:
                yield combine_names_rows(column_names, rows)
                rows = []
                chunk_end += chunksize
        else:
            if len(rows) > 0:
                yield combine_names_rows(column_names, rows)


def read_csv_file(
    path: str,
    newline='',
    encoding='utf-8-sig'
) -> dict:
    with open(path, 'r', newline=newline, encoding=encoding) as f:
        return row_dicts_to_data([row for row in csv.DictReader(f)])


def data_to_csv_file(
    data: MutableMapping,
    path: str,
    newline='',
    encoding='utf-8-sig'
) -> None:
    """Write data to csv file at path."""
    names = column_names(data)
    rows = itertuples(data)
    with open(path, 'w', encoding=encoding, newline=newline) as f:
        writer = csv.writer(f)
        writer.writerow(names)
        writer.writerows(rows)
