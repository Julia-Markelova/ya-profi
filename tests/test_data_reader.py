from pathlib import Path
import pytest
from app.data_reader import DataReader

import csv

data_reader = DataReader()


def test_read_from_non_existing_file():
    with pytest.raises(Exception):
        data_reader.read_from_file('no such file', 0, '')


def test_from_csv():
    path = Path('test.csv')
    with open(str(path), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow('1, 2')
    df = data_reader.read_from_file(str(path), 0)
    assert df is not None

