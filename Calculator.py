class Calculator:
    """All calculation logic for electricity bills."""
    
    @staticmethod
    def compute_consumption(prev_reading, curr_reading):
        if curr_reading < prev_reading:
            raise ValueError("Current reading cannot be less than previous reading.")
        return curr_reading - prev_reading

    @staticmethod
    def compute_kwh_price(amount, consumption):
        return round(amount / consumption, 2) if consumption > 0 else 0.0