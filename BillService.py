from RecordRepository import RecordRepository
from Record import Record

class BillService:
    def __init__(self, repository: RecordRepository):
        self.repository = repository

    def add_record(self, year, month, prev_reading, curr_reading, amount):
        record = Record(year, month, prev_reading, curr_reading, amount)
        self.repository.save(record)
        return record