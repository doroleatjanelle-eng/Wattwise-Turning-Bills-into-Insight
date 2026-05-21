import csv
import os
import pandas as pd
from Record import Record, FILENAME, HEADER
from RecordRepository import RecordRepository

MONTHS = {
    1: 'JANUARY', 2: 'FEBRUARY', 3: 'MARCH', 4: 'APRIL',
    5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUGUST',
    9: 'SEPTEMBER', 10: 'OCTOBER', 11: 'NOVEMBER', 12: 'DECEMBER'
}

class Summary:
    def __init__(self, repository: RecordRepository):
        self.repository = repository

    def generate_summary(self, year):
        try:
            df = self.repository.load_all()
            if df.empty:
                print("No records found in the database.")
                return

            df_year = df[df['Year'] == year]
            if df_year.empty:
                print(f"No records found for year {year}.")
                return

            month_order = list(MONTHS.values())
            df_year['Month'] = pd.Categorical(df_year['Month'], categories=month_order, ordered=True)
            df_year = df_year.sort_values('Month')

            total_consumption = df_year['Units Consumed'].sum()
            total_cost = df_year['Amount'].sum()
            avg_kwh_price = total_cost / total_consumption if total_consumption > 0 else 0
            avg_monthly_consumption = total_consumption / len(df_year) if len(df_year) > 0 else 0

            max_consumption_row = df_year.loc[df_year['Units Consumed'].idxmax()] if not df_year.empty else None
            min_consumption_row = df_year.loc[df_year['Units Consumed'].idxmin()] if not df_year.empty else None
            max_cost_row = df_year.loc[df_year['Amount'].idxmax()] if not df_year.empty else None
            min_cost_row = df_year.loc[df_year['Amount'].idxmin()] if not df_year.empty else None

            print("\n" + "=" * 60)
            print(f"           YEAR-END SUMMARY FOR {year}")
            print("=" * 60)

            print(f"\n{'MONTH':<12} {'UNITS':>8} {'AMOUNT (PHP)':>14} {'KWH PRICE':>10}")
            print("-" * 50)
            for _, row in df_year.iterrows():
                print(f"{row['Month']:<12} {row['Units Consumed']:>8} {row['Amount']:>14.2f} {row['Kwh Price']:>10.2f}")

            print("-" * 50)
            print(f"{'TOTAL / AVG':<12} {total_consumption:>8} {total_cost:>14.2f} {avg_kwh_price:>10.2f}")
            print(f"\nAverage monthly consumption: {avg_monthly_consumption:.2f} units")

            if max_consumption_row is not None:
                print(f"\n📈 Highest consumption: {max_consumption_row['Units Consumed']} units ({max_consumption_row['Month']})")
            if min_consumption_row is not None:
                print(f"📉 Lowest consumption: {min_consumption_row['Units Consumed']} units ({min_consumption_row['Month']})")
            if max_cost_row is not None:
                print(f"💰 Highest bill: PHP {max_cost_row['Amount']:.2f} ({max_cost_row['Month']})")
            if min_cost_row is not None:
                print(f"💸 Lowest bill: PHP {min_cost_row['Amount']:.2f} ({min_cost_row['Month']})")

            if len(df_year) < 12:
                missing = 12 - len(df_year)
                print(f"\n⚠️ Warning: Data for {missing} month(s) missing in {year}.")
            else:
                print("\n✅ Complete data for all 12 months.")

            prev_year = year - 1
            df_prev = df[df['Year'] == prev_year]
            if not df_prev.empty:
                prev_total_consumption = df_prev['Units Consumed'].sum()
                prev_total_cost = df_prev['Amount'].sum()
                print("\n--- COMPARISON WITH PREVIOUS YEAR ---")
                print(f"{prev_year} total consumption: {prev_total_consumption} units")
                change_consumption = total_consumption - prev_total_consumption
                print(f"{year} total consumption: {total_consumption} units ({change_consumption:+.0f} units, {(change_consumption/prev_total_consumption)*100:+.1f}%)")
                print(f"{prev_year} total cost: PHP {prev_total_cost:.2f}")
                change_cost = total_cost - prev_total_cost
                print(f"{year} total cost: PHP {total_cost:.2f} ({change_cost:+.2f} PHP, {(change_cost/prev_total_cost)*100:+.1f}%)")

            print("=" * 60 + "\n")
        except Exception as e:
            print(f"Error generating summary: {e}")