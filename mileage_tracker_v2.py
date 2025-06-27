import json
import os
from datetime import datetime

DATA_FILE = "bike_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def input_float(prompt, allow_zero=False):
    while True:
        try:
            val = float(input(prompt))
            if val < 0 or (not allow_zero and val == 0):
                print("Please enter a positive number.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a number.")

def input_date(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD) or leave empty for today: ")
        if date_str.strip() == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")

def add_entry(data, with_oil=True):
    date = input_date("Enter the date")
    total_km = input_float("Enter total kilometers on the bike: ")

    # Validate total_km is >= last entry's total_km
    if data and total_km < data[-1]["total_km"]:
        print(f"Error: Total kilometers ({total_km}) cannot be less than last recorded ({data[-1]['total_km']}).")
        return

    oil_liters = 0.0
    oil_cost = 0.0
    if with_oil:
        oil_liters = input_float("Enter oil liters bought: ", allow_zero=True)
        oil_cost = input_float("Enter cost of oil bought: ", allow_zero=True)

    entry = {
        "date": date,
        "total_km": total_km,
        "oil_liters": oil_liters,
        "oil_cost": oil_cost
    }

    data.append(entry)
    save_data(data)
    print("Entry added successfully!\n")

def view_history(data):
    if not data:
        print("No history yet.")
        return
    print("\n--- Bike History ---")
    for i, entry in enumerate(data):
        print(f"{i+1}. Date: {entry['date']}, Total KM: {entry['total_km']}, Oil: {entry['oil_liters']}L, Cost: {entry['oil_cost']}")
    print()

def calculate_stats(data):
    if len(data) < 2:
        print("Not enough data to calculate stats. Add at least two entries.")
        return

    total_distance = data[-1]["total_km"] - data[0]["total_km"]
    total_oil = sum(entry["oil_liters"] for entry in data)
    total_cost = sum(entry["oil_cost"] for entry in data)

    # Calculate mileage weighted by each oil fill interval
    mileage_list = []
    for i in range(1, len(data)):
        dist = data[i]["total_km"] - data[i-1]["total_km"]
        oil = data[i]["oil_liters"]
        if oil > 0:
            mileage_list.append(dist / oil)

    avg_mileage = sum(mileage_list) / len(mileage_list) if mileage_list else 0
    avg_cost_per_km = total_cost / total_distance if total_distance > 0 else 0

    print("\n--- Statistics ---")
    print(f"Total distance ridden: {total_distance:.2f} km")
    print(f"Total oil consumed: {total_oil:.2f} liters")
    print(f"Total money spent on oil: {total_cost:.2f} money units")
    print(f"Average mileage: {avg_mileage:.2f} km/liter")
    print(f"Average cost per km: {avg_cost_per_km:.2f} money units")
    print()

def export_csv(data):
    if not data:
        print("No data to export.")
        return

    filename = input("Enter filename to export CSV (e.g. bike_data.csv): ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, "w") as f:
            f.write("Date,Total KM,Oil Liters,Oil Cost\n")
            for entry in data:
                f.write(f"{entry['date']},{entry['total_km']},{entry['oil_liters']},{entry['oil_cost']}\n")
        print(f"Data exported to {filename}\n")
    except Exception as e:
        print(f"Error exporting CSV: {e}\n")

def main_menu():
    data = load_data()

    while True:
        print("=== Bike Mileage & Oil Tracker ===")
        print("1. Add new entry (with oil purchase)")
        print("2. Add new ride only (no oil purchase)")
        print("3. View history")
        print("4. Show statistics")
        print("5. Export data to CSV")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            add_entry(data, with_oil=True)
        elif choice == '2':
            add_entry(data, with_oil=False)
        elif choice == '3':
            view_history(data)
        elif choice == '4':
            calculate_stats(data)
        elif choice == '5':
            export_csv(data)
        elif choice == '6':
            print("Goodbye! Stay safe on the road.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.\n")

if __name__ == "__main__":
    main_menu()
