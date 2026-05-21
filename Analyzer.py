import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from Record import Record, FILENAME, HEADER
from RecordRepository import RecordRepository   # for type hint

MONTHS = {
    1: 'JANUARY', 2: 'FEBRUARY', 3: 'MARCH', 4: 'APRIL',
    5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUGUST',
    9: 'SEPTEMBER', 10: 'OCTOBER', 11: 'NOVEMBER', 12: 'DECEMBER'
}

class Analyzer:
    def __init__(self, repository: RecordRepository):
        self.repository = repository

    def compare_last_two_records(self):
        try:
            if not os.path.exists(self.repository.filename):
                print("No records found.")
                return

            with open(self.repository.filename, 'r', newline="") as file:
                reader = list(csv.reader(file))
                if len(reader) <= 2:
                    print("Not enough records to compare.")
                    return

                last_row = reader[-1]
                prev_row = reader[-2]

                prev_month, prev_units, prev_price = prev_row[1], float(prev_row[5]), float(prev_row[4])
                curr_month, curr_units, curr_price = last_row[1], float(last_row[5]), float(last_row[4])

                print("========= COMPARING LAST TWO RECORDS =========")
                print(f"{prev_month} CONSUMPTION: {prev_units} units | KWh Price: {prev_price}")
                print(f"{curr_month} CONSUMPTION: {curr_units} units | KWh Price: {curr_price}")
                print("==============================================\n")

                print("=========== REMARK ===========")
                if curr_units > prev_units:
                    diff = curr_units - prev_units
                    print(f"You consumed MORE electricity this month (+{diff:.1f} units).")
                elif curr_units < prev_units:
                    diff = prev_units - curr_units
                    print(f"You consumed LESS electricity this month (-{diff:.1f} units).")
                else:
                    print("Your consumption is the SAME as last month.")

                if curr_price > prev_price:
                    print("⚠️ KWh price is HIGHER this month. Consider reducing consumption to save costs.")
                elif curr_price < prev_price:
                    print("✅ KWh price is LOWER this month. Good time to optimize usage.")
                else:
                    print("ℹ️ KWh price is the SAME as last month.")
        except Exception as e:
            print(f"Error during comparison: {e}")

    def plot_trend(self):
        """Generate a line graph showing consumption and bill amount over time."""
        try:
            df = self.repository.load_all()
            if df.empty:
                print("No records to plot.")
                return

            month_to_num = {v: k for k, v in MONTHS.items()}   # uses MONTHS
            df['Month_Num'] = df['Month'].map(month_to_num)
            df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month_Num'].astype(str), format='%Y-%m')
            df = df.sort_values('Date')

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

            ax1.plot(df['Date'], df['Units Consumed'], marker='o', color='tab:blue', linewidth=2)
            ax1.set_ylabel('Consumption (units)', fontsize=12)
            ax1.set_title('Monthly Electricity Consumption Trend', fontsize=14)
            ax1.grid(True, linestyle='--', alpha=0.6)
            for i, row in df.iterrows():
                ax1.annotate(str(row['Units Consumed']), (row['Date'], row['Units Consumed']),
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

            ax2.plot(df['Date'], df['Amount'], marker='s', color='tab:red', linewidth=2)
            ax2.set_ylabel('Bill Amount (PHP)', fontsize=12)
            ax2.set_title('Monthly Bill Amount Trend', fontsize=14)
            ax2.grid(True, linestyle='--', alpha=0.6)
            for i, row in df.iterrows():
                ax2.annotate(f"{row['Amount']:.2f}", (row['Date'], row['Amount']),
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

            plt.xticks(rotation=45)
            ax2.set_xlabel('Billing Month', fontsize=12)

            plt.tight_layout()
            plt.show(block=False)
            plt.pause(10)
            plt.close()

        except Exception as e:
            print(f"Error generating graph: {e}")
        # Removed the stray print that caused NameError