import datetime
import calendar
import json
from collections import defaultdict

def format_currency(amount):
    return f"${amount:,.2f}"

def validate_month_input(month_str):
    """Validate input like '2024-01' and return datetime.date set to first day of that month."""
    try:
        dt = datetime.datetime.strptime(month_str, "%Y-%m")
        return dt.date()
    except ValueError:
        return None

def get_month_name_year(date_obj):
    return f"{calendar.month_name[date_obj.month]} {date_obj.year}"

def input_positive_float(prompt):
    while True:
        val = input(prompt).strip()
        try:
            fval = float(val)
            if fval < 0:
                print("Please enter a positive amount or zero.")
            else:
                return fval
        except ValueError:
            print("Invalid number, please try again.")

def input_month(prompt):
    while True:
        month_str = input(prompt).strip()
        dt = validate_month_input(month_str)
        if dt:
            return month_str
        else:
            print("Invalid month format. Use YYYY-MM.")

def print_bar_chart(items, max_width=20):
    """Print text bar chart for dict items with numeric values.

    Items: list of (label, value)
    Bars scaled to max_width length for largest value.
    """
    if not items:
        print("(No data)")
        return
    max_val = max(v for _, v in items)
    if max_val == 0:
        max_val = 1  # Avoid div by zero
    for label, val in items:
        # Bar length scaled to max_width
        bar_len = int(val / max_val * max_width)
        bar = "█" * bar_len + "░" * (max_width - bar_len)
        percent = (val / max_val * 100) if max_val else 0
        print(f"{label:<12} {bar} {format_currency(val)} ({percent:.1f}%)")

def export_month_summary(data, budgets, month):
    filename = f"budget_summary_{month}.txt"
    with open(filename, "w") as f:
        f.write(f"=== PERSONAL BUDGET TRACKER ===\nMonth: {get_month_name_year(datetime.datetime.strptime(month, '%Y-%m'))}\n\n")
        total_income = sum(data.get(month, {}).get("income", {}).values()) if month in data else 0
        total_expenses = sum(data.get(month, {}).get("expenses", {}).values()) if month in data else 0
        net = total_income - total_expenses
        net_pct = (net / total_income * 100) if total_income else 0

        f.write("💰 FINANCIAL SUMMARY\n")
        f.write(f"Total Income: {format_currency(total_income)}\n")
        f.write(f"Total Expenses: {format_currency(total_expenses)}\n")
        f.write(f"Net Savings: {format_currency(net)} ({net_pct:.1f}%)\n\n")

        f.write("📊 EXPENSE BREAKDOWN\n")
        expenses = data.get(month, {}).get("expenses", {})
        total_exp = total_expenses if total_expenses != 0 else 1
        sorted_exp = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        max_val = max([v for _, v in sorted_exp], default=1)
        max_width = 20
        for cat, amt in sorted_exp:
            bar_len = int(amt / max_val * max_width)
            bar = "█" * bar_len + "░" * (max_width - bar_len)
            percent = (amt / total_exp * 100)
            f.write(f"{cat:<12} {bar} {format_currency(amt)} ({percent:.1f}%)\n")

        # Budget alerts
        f.write("\n⚠️ BUDGET ALERTS:\n")
        alerts_found = False
        month_budgets = budgets.get(month, {})
        for cat, limit in month_budgets.items():
            spent = expenses.get(cat, 0)
            if spent > limit:
                alerts_found = True
                over_amt = spent - limit
                percent_of_limit = (spent / limit * 100)
                f.write(f"{cat}: {format_currency(over_amt)} over budget ({percent_of_limit:.1f}% of limit)\n")
        if not alerts_found:
            f.write("No budget alerts.\n")

    print(f"Monthly summary exported to {filename}")

def analyze_trends(data, category, months_list, category_type):
    """Analyze spending or income trend for category over months in months_list."""
    values = []
    for m in months_list:
        month_data = data.get(m, {})
        cat_values = month_data.get(category_type, {})
        values.append(cat_values.get(category, 0))

    if len(values) < 2:
        return "No trend data"

    # Simple linear trend: compare last value to first value
    if values[-1] > values[0]:
        return "Increasing"
    elif values[-1] < values[0]:
        return "Decreasing"
    else:
        return "Stable"

def main():
    data = {}  # structure: {"YYYY-MM": {"income": {}, "expenses": {}}}
    budgets = {}  # monthly budget limits by category, same month keys, {"YYYY-MM": {"food": 400, ...}}

    print("=== PERSONAL BUDGET TRACKER ===")

    # Pre-fill some test months for easy demo or let user enter data.
    # Uncomment to seed with some example data:
    # data["2024-01"] = {"income": {"salary": 3200}, "expenses": {"Food": 430, "Transport": 200, "Housing": 800}}
    # budgets["2024-01"] = {"Food": 400, "Transport": 220, "Housing": 850}

    def total_by_type(month, tipe):
        return sum(data.get(month, {}).get(tipe, {}).values())

    while True:
        print("\nOptions:")
        print("1. Add income")
        print("2. Add expense")
        print("3. Set monthly budget limit")
        print("4. View month summary")
        print("5. Export month summary to file")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            month = input_month("Enter month for income (YYYY-MM): ")
            inc_cat = input("Income category (e.g., salary, bonus): ").strip()
            amount = input_positive_float("Income amount: $")
            data.setdefault(month, {}).setdefault("income", {})
            data[month]["income"][inc_cat] = data[month]["income"].get(inc_cat, 0) + amount
            print(f"Added income: {inc_cat} ${amount:,.2f} for {month}")

        elif choice == "2":
            month = input_month("Enter month for expense (YYYY-MM): ")
            exp_cat = input("Expense category (e.g., Food, Transport): ").strip()
            amount = input_positive_float("Expense amount: $")
            data.setdefault(month, {}).setdefault("expenses", {})
            data[month]["expenses"][exp_cat] = data[month]["expenses"].get(exp_cat, 0) + amount
            print(f"Added expense: {exp_cat} ${amount:,.2f} for {month}")

        elif choice == "3":
            month = input_month("Set budget month (YYYY-MM): ")
            cat = input("Category to set budget for: ").strip()
            limit = input_positive_float("Budget limit amount: $")
            budgets.setdefault(month, {})
            budgets[month][cat] = limit
            print(f"Set budget for {cat} at {format_currency(limit)} in {month}")

        elif choice == "4":
            month = input_month("Enter month to view summary (YYYY-MM): ")
            month_data = data.get(month, {"income": {}, "expenses": {}})
            month_budgets = budgets.get(month, {})

            print(f"\nMonth: {get_month_name_year(datetime.datetime.strptime(month, '%Y-%m'))}\n")

            total_income = sum(month_data.get("income", {}).values())
            total_expenses = sum(month_data.get("expenses", {}).values())
            net = total_income - total_expenses
            net_pct = (net / total_income * 100) if total_income else 0

            print("💰 FINANCIAL SUMMARY")
            print(f"Total Income: {format_currency(total_income)}")
            print(f"Total Expenses: {format_currency(total_expenses)}")
            print(f"Net Savings: {format_currency(net)} ({net_pct:.1f}%)\n")

            print("📊 EXPENSE BREAKDOWN")
            expenses = month_data.get("expenses", {})
            if not expenses:
                print("(No expenses recorded)")
            else:
                total_exp = total_expenses if total_expenses != 0 else 1
                sorted_exp = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
                print_bar_chart(sorted_exp)

            # Budget alerts
            print("\n⚠️ BUDGET ALERTS:")
            alerts_found = False
            for cat, limit in month_budgets.items():
                spent = expenses.get(cat, 0)
                if spent > limit:
                    alerts_found = True
                    over_amt = spent - limit
                    percent_of_limit = (spent / limit * 100)
                    print(f"{cat}: {format_currency(over_amt)} over budget ({percent_of_limit:.1f}% of limit)")
            if not alerts_found:
                print("No budget alerts.")

            # Spending trend analysis
            print("\n📈 SPENDING TREND ANALYSIS:")
            # Analyze previous 3 months if possible to detect trend for each category in this month expenses and budgets
            try:
                dt = datetime.datetime.strptime(month, "%Y-%m")
                months_for_trends = []
                for i in range(3, 0, -1):
                    prev_month = (dt.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
                    for _ in range(i-1):
                        prev_month = (prev_month.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
                    months_for_trends.append(prev_month.strftime("%Y-%m"))
            except Exception:
                months_for_trends = []

            categories_set = set(expenses.keys()).union(month_budgets.keys())

            if not months_for_trends:
                print("(Not enough data for trend analysis)")
            else:
                for cat in categories_set:
                    trend = analyze_trends(data, cat, months_for_trends + [month], "expenses")
                    print(f"{cat}: {trend}")

        elif choice == "5":
            month = input_month("Enter month to export summary (YYYY-MM): ")
            export_month_summary(data, budgets, month)

        elif choice == "6":
            print("Exiting budget tracker. Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number from 1-6.")

if __name__ == "__main__":
    main()
