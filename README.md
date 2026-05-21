## Wattwise: Turning Bills Into Insight

## Application Description

Wattwise is a Python-based command-line application that helps users track, analyse, and visualise their monthly electricity bills.  
It automatically calculates energy consumption and cost per kilowatt-hour (kWh), compares month‑to‑month usage, generates trend graphs, and produces detailed year‑end summaries – turning raw bill data into actionable insights.

## The Application Allows User To

- Add new electricity bill records (year, month, meter readings, total amount)
- Automatically compute **units consumed** and **kWh price**
- Compare the last two months’ consumption and rate
- View a graphical trend of consumption and bill amount over time
- Generate a year‑end summary with totals, averages, highest/lowest months, and year‑over‑year comparison

## OOP Concepts Used

- **Encapsulation** – Each class (`Record`, `RecordRepository`, `Analyzer`, etc.) hides internal data and exposes only necessary methods.  
  Example: `Record` uses private attributes (`_year`, `_month`, etc.) with `@property` getters/setters for validation.

- **Abstraction** – The `Calculator` class provides static methods (`compute_consumption`, `compute_kwh_price`) that hide the complex arithmetic logic.

- **Composition** – `WattwiseApp` contains instances of `RecordRepository`, `BillService`, `Analyzer`, and `Summary`, delegating responsibilities rather than inheriting.

- **Separation of Concerns** – Each class has a single, well-defined responsibility (e.g., `RecordRepository` handles only CSV I/O, `Analyzer` handles only comparisons and plots).

## Technologies Used

- **Language:** Python 3.7+
- **Libraries:**
  - `pandas` – data manipulation and aggregation for summaries
  - `matplotlib` – generating consumption and bill trend graphs
  - `csv` (standard library) – reading/writing CSV files
- **Storage:** CSV file (`watt_record.csv`)

## Project Structure

```
wattwise/
├── WattwiseApp.py          # Main application entry point (CLI menu)
├── BillService.py          # Orchestrates record creation
├── Record.py               # Record class with validation & computed properties
├── RecordRepository.py     # CSV read/write operations
├── Analyzer.py             # Month‑to‑month comparison + trend plotting
├── Summary.py              # Year‑end summary generation
├── Calculator.py           # Static methods for consumption & kWh price
├── watt_record.csv         # Auto‑generated data file (created on first run)
└── README.md
```

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wattwise.git
   cd wattwise
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install pandas matplotlib
   ```

4. **Run the application**
   ```bash
   python WattwiseApp.py
   ```

5. **Follow the on‑screen menu** to add records, compare months, view graphs, or generate year summaries.

---

## Features (Detailed)

- 📝 **Add new bill records** – store year, month, previous/current readings, and amount.
- 🧮 **Consumption and cost calculator** – automatically computes units consumed (current – previous) and kWh price (amount / consumption).
- 🔍 **Compare last two months** – shows changes in consumption and kWh price with smart remarks.
- 📈 **Trend graphs** – visualises consumption and bill amount over time using `matplotlib`.
- 📊 **Year‑end summary** – total consumption, average cost, highest/lowest months, and comparison with previous year.

## Example Output (Year‑end summary)

```
============================================================
           YEAR-END SUMMARY FOR 2025
============================================================

MONTH        UNITS   AMOUNT (PHP)   KWH PRICE
--------------------------------------------------
JANUARY        320         2500.00        7.81
FEBRUARY       290         2280.00        7.86
...
--------------------------------------------------
TOTAL / AVG   3650        28500.00        7.81

Average monthly consumption: 304.17 units

📈 Highest consumption: 350 units (MAY)
📉 Lowest consumption: 270 units (DECEMBER)
💰 Highest bill: PHP 2850.00 (MAY)
💸 Lowest bill: PHP 2100.00 (DECEMBER)

✅ Complete data for all 12 months.

```
---

**Made with ⚡ for smarter energy tracking.**
```
