import csv
import os
import pandas as pd
from Record import Record, FILENAME, HEADER

class RecordRepository:
    def __init__(self, filename=FILENAME):
        self.filename = filename
        try:
            if not os.path.exists(filename):
                with open(filename, 'w', newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(HEADER)
        except (IOError, OSError) as e:
            raise RuntimeError(f"Cannot create or open data file: {e}")

    def save(self, record: Record):
        try:
            with open(self.filename, 'a', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(record.to_row())
        except (IOError, OSError, csv.Error) as e:
            raise RuntimeError(f"Failed to save record: {e}")

    def load_all(self):
        try:
            return pd.read_csv(self.filename)
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise RuntimeError(f"Failed to load data: {e}")

    def get_last_prev_reading(self):
        if not os.path.exists(self.filename):
            return None
        try:
            with open(self.filename, 'r', newline="") as file:
                reader = list(csv.reader(file))
                if len(reader) <= 1:
                    return None
                return float(reader[-1][3])
        except (IOError, csv.Error, ValueError, IndexError) as e:
            raise RuntimeError(f"Failed to read last previous reading: {e}")