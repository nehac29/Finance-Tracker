import pandas as pd
import src.database as db


def fetch_transactions_df(user_id=None):
    """Fetch transactions from DB and return as Pandas DataFrame."""
    rows = db.get_transactions(user_id)
    if not rows:
        return pd.DataFrame()

    # Map columns based on DB schema
    columns = ["txn_id", "user_id", "date", "amount", "type", "category_id", "description", "tags"]
    df = pd.DataFrame(rows, columns=columns)

    # Convert date and amount to appropriate types
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])

    return df


def aggregate_monthly_summary(df):
    """Aggregate monthly income, expenses, and net savings."""
    if df.empty:
        return pd.DataFrame()

    # Add year-month column for grouping
    df['year_month'] = df['date'].dt.to_period('M')

    # Group by year_month and type, summing amounts
    summary = df.groupby(['year_month', 'type'])['amount'].sum().unstack(fill_value=0)

    # Calculate net savings = income - expense
    summary['net_savings'] = summary.get('income', 0) - summary.get('expense', 0)

    return summary.reset_index()


def category_wise_spending(df):
    """Calculate total spending by category."""
    if df.empty:
        return pd.DataFrame()

    # Filter only expenses
    expenses = df[df['type'] == 'expense']

    # Join with category names
    categories = db.execute_query("SELECT category_id, name FROM categories")
    if categories:
        cat_map = {cid: name for cid, name in categories}
        expenses['category_name'] = expenses['category_id'].map(cat_map)
    else:
        expenses['category_name'] = None

    # Aggregate amount by category_name
    category_sums = expenses.groupby('category_name')['amount'].sum().sort_values(ascending=False)
    return category_sums.reset_index()


def budget_compliance_report(user_id=None):
    """Check spending against set budgets."""
    df = fetch_transactions_df(user_id)
    if df.empty:
        return pd.DataFrame()

    budgets = db.execute_query("SELECT category_id, amount, start_date, end_date FROM budgets WHERE user_id = ?", (user_id,))
    if not budgets:
        print("No budgets found.")
        return pd.DataFrame()

    # Convert budgets list to DataFrame
    budgets_df = pd.DataFrame(budgets, columns=['category_id', 'budget_amount', 'start_date', 'end_date'])
    budgets_df['start_date'] = pd.to_datetime(budgets_df['start_date'])
    budgets_df['end_date'] = pd.to_datetime(budgets_df['end_date'])

    report_rows = []

    for _, budget in budgets_df.iterrows():
        # Filter transactions in budget period and category
        mask = (
            (df['category_id'] == budget['category_id']) &
            (df['type'] == 'expense') &
            (df['date'] >= budget['start_date']) &
            (df['date'] <= budget['end_date'])
        )
        total_spent = df.loc[mask, 'amount'].sum()
        remaining = budget['budget_amount'] - total_spent

        report_rows.append({
            'category_id': budget['category_id'],
            'budget_amount': budget['budget_amount'],
            'total_spent': total_spent,
            'remaining': remaining
        })

    report_df = pd.DataFrame(report_rows)

    # Map category names
    categories = db.execute_query("SELECT category_id, name FROM categories")
    if categories:
        cat_map = {cid: name for cid, name in categories}
        report_df['category_name'] = report_df['category_id'].map(cat_map)

    return report_df[['category_name', 'budget_amount', 'total_spent', 'remaining']]


if __name__ == "__main__":
    # Example usage
    df = fetch_transactions_df()
    print("Monthly summary:")
    print(aggregate_monthly_summary(df))

    print("\nCategory spending:")
    print(category_wise_spending(df))

    print("\nBudget compliance report:")
    print(budget_compliance_report())
