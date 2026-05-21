from RecordRepository import RecordRepository
from Analyzer import Analyzer
from Summary import Summary
from BillService import BillService   # ✅ import the class

MONTHS = {
    1: 'JANUARY', 2: 'FEBRUARY', 3: 'MARCH', 4: 'APRIL',
    5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUGUST',
    9: 'SEPTEMBER', 10: 'OCTOBER', 11: 'NOVEMBER', 12: 'DECEMBER'
}

class WattWiseApp:
    def __init__(self):
        try:
            self.repo = RecordRepository()
            self.service = BillService(self.repo)   # Use class from module
            self.analyzer = Analyzer(self.repo)
            self.summary = Summary(self.repo)
        except RuntimeError as e:
            print(f"Critical error starting application: {e}")
            raise

    def display_months(self):
        print("========= MONTHS =========")
        keys = list(MONTHS.keys())
        for i in range(0, len(keys), 2):
            k1, v1 = keys[i], MONTHS[keys[i]]
            if i + 1 < len(keys):
                k2, v2 = keys[i+1], MONTHS[keys[i+1]]
                print(f"{k1}: {v1:<10} | {k2}: {v2}")
            else:
                print(f"{k1}: {v1}")
        print("==========================")

    def show_menu(self):
        print("\n========= MENU =========")
        print("1. Add new bill record")
        print("2. Compare last two months")
        print("3. View consumption & amount trend graph")
        print("4. View year-end summary")
        print("5. Exit")
        print("=======================")

    def run(self):
        while True:
            try:
                self.show_menu()
                choice = input("Enter your choice (1-5): ").strip()

                if choice == '1':
                    self.add_new_record()
                elif choice == '2':
                    self.analyzer.compare_last_two_records()
                elif choice == '3':
                    print("Close the graph window to return to the menu.")
                    self.analyzer.plot_trend()
                elif choice == '4':
                    self.view_year_summary()
                elif choice == '5':
                    print("Thank you for using WattWise! Goodbye.")
                    break
                else:
                    print("Invalid choice. Please enter 1,2,3,4 or 5.")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user. Returning to menu.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def add_new_record(self):
        print("\n========= ADD NEW ELECTRICITY BILL =========")
        try:
            year = int(input("Enter year: "))
            if year < 1900 or year > 2100:
                print("Invalid year. Please enter a year between 1900 and 2100.")
                return

            self.display_months()
            month_num = int(input("Select month (1-12): "))
            if month_num not in MONTHS:
                print("Invalid month.")
                return

            try:
                last_prev = self.repo.get_last_prev_reading()
            except RuntimeError as e:
                print(f"Warning: {e}. Proceeding with manual input.")
                last_prev = None

            if last_prev is not None:
                prev_reading = last_prev
                print(f"(Auto-filled) Previous reading: {prev_reading}")
            else:
                prev_reading = float(input("No previous record found.\nEnter PREVIOUS READING manually: "))

            curr_reading = float(input("Enter current reading: "))
            if curr_reading < prev_reading:
                print("Error: Current reading cannot be less than previous reading.")
                return

            amount = float(input("Enter bill amount: "))
            if amount <= 0:
                print("Error: Bill amount must be a positive number.")
                return

            record = self.service.add_record(year, month_num, prev_reading, curr_reading, amount)
            print(f"✅ Saved: {record.to_row()}")
            print("Record added successfully!\n")
        except ValueError as e:
            print(f"Input error: {e}")
        except RuntimeError as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error while adding record: {e}")

    def view_year_summary(self):
        try:
            year = int(input("Enter year for summary (e.g., 2025): "))
            self.summary.generate_summary(year)
        except ValueError:
            print("Invalid year. Please enter a whole number.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        WattWiseApp().run()
    except Exception as e:
        print(f"Fatal error: {e}")