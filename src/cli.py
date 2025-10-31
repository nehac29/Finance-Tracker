import argparse
import datetime
import src.etl as etl
import src.analytics as analytics
import src.export as export
import src.database as db


def add_transaction_interactive():
    """Prompt user to enter transaction details and add to DB."""
    print("Add New Transaction")
    date_str = input("Date (YYYY-MM-DD) [default today]: ").strip()
    if not date_str:
        date_str = datetime.datetime.today().strftime("%Y-%m-%d")

    amount_str = input("Amount: ").strip()
    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount entered.")
        return

    txn_type = input("Type (income/expense/investment): ").lower().strip()
    if txn_type not in ['income', 'expense', 'investment']:
        print("Invalid type entered.")
        return

    category = input("Category (optional): ").strip()
    description = input("Description (optional): ").strip()
    tags = input("Tags (comma separated, optional): ").strip()

    # Resolve category ID or None
    category_id = None
    if category:
        category_id = db.execute_query("SELECT category_id FROM categories WHERE name = ?", (category,))
        if not category_id:
            # Create category if not existing
            db.execute_query("INSERT INTO categories (name) VALUES (?)", (category,))
            category_id = db.execute_query("SELECT category_id FROM categories WHERE name = ?", (category,))
        category_id = category_id[0][0]

    db.add_transaction(
        date=date_str,
        amount=amount,
        txn_type=txn_type,
        category_id=category_id,
        description=description if description else None,
        tags=tags if tags else None,
    )
    print("Transaction added successfully.")


def view_summary():
    """Show monthly summary and category-wise spending."""
    df = analytics.fetch_transactions_df()
    if df.empty:
        print("No transactions found.")
        return

    monthly_summary = analytics.aggregate_monthly_summary(df)
    print("\nMonthly Summary:")
    print(monthly_summary)

    category_spending = analytics.category_wise_spending(df)
    print("\nCategory-wise Spending:")
    print(category_spending)


def export_reports():
    """Export reports to CSV and Excel for Power BI."""
    df = analytics.fetch_transactions_df()
    if df.empty:
        print("No transactions found for export.")
        return

    monthly_summary = analytics.aggregate_monthly_summary(df)
    category_spending = analytics.category_wise_spending(df)

    export.export_to_csv(monthly_summary, "monthly_summary.csv")
    export.export_to_excel(monthly_summary, "monthly_summary.xlsx")

    export.export_to_csv(category_spending, "category_spending.csv")
    export.export_to_excel(category_spending, "category_spending.xlsx")


def main():
    parser = argparse.ArgumentParser(description="Advanced Personal Finance Tracker CLI")
    parser.add_argument('--add', action='store_true', help='Add a new financial transaction')
    parser.add_argument('--summary', action='store_true', help='View financial summaries')
    parser.add_argument('--export', action='store_true', help='Export reports for Power BI')

    args = parser.parse_args()

    if args.add:
        add_transaction_interactive()
    elif args.summary:
        view_summary()
    elif args.export:
        export_reports()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
