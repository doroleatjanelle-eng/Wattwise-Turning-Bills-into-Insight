from Calculator import Calculator

FILENAME = 'watt_record.csv'
HEADER = ["Year", "Month", "Prev Reading", "Curr Reading", "Kwh Price", "Units Consumed", "Amount"]

MONTHS = {
    1: 'JANUARY', 2: 'FEBRUARY', 3: 'MARCH', 4: 'APRIL',
    5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUGUST',
    9: 'SEPTEMBER', 10: 'OCTOBER', 11: 'NOVEMBER', 12: 'DECEMBER'
}

class Record:
    def __init__(self, year, month, prev_reading, curr_reading, amount):
        self.year = year
        self.month = month
        self.prev_reading = prev_reading
        self.curr_reading = curr_reading
        self.amount = amount

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 1900 or value > 2100:
            raise ValueError("Year must be an integer between 1900 and 2100.")
        self._year = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        if not isinstance(value, int) or value not in MONTHS:
            raise ValueError(f"Month must be 1..12, got {value}.")
        self._month = value

    @property
    def month_name(self):
        return MONTHS[self.month]

    @property
    def prev_reading(self):
        return self._prev_reading

    @prev_reading.setter
    def prev_reading(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Previous reading must be >= 0.")
        self._prev_reading = value

    @property
    def curr_reading(self):
        return self._curr_reading

    @curr_reading.setter
    def curr_reading(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Current reading must be >= 0.")
        if hasattr(self, '_prev_reading') and value < self.prev_reading:
            raise ValueError(f"Current ({value}) cannot be less than previous ({self.prev_reading}).")
        self._curr_reading = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Bill amount must be positive.")
        self._amount = value

    @property
    def consumption(self):
        return Calculator.compute_consumption(self.prev_reading, self.curr_reading)

    @property
    def kwh_price(self):
        return Calculator.compute_kwh_price(self.amount, self.consumption)

    def to_row(self):
        return [
            self.year,
            self.month_name,
            self.prev_reading,
            self.curr_reading,
            round(self.kwh_price, 2),
            self.consumption,
            self.amount
        ]