import os
import pandas as pd

EXPORT_DIR = "data/export"

# Ensure the export directory exists
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_to_csv(df, filename):
    """Export DataFrame to CSV file in export directory."""
    if df.empty:
        print("Warning: Empty DataFrame, nothing to export.")
        return
    file_path = os.path.join(EXPORT_DIR, filename)
    df.to_csv(file_path, index=False)
    print(f"Data exported to CSV: {file_path}")


def export_to_excel(df, filename):
    """Export DataFrame to Excel file in export directory."""
    if df.empty:
        print("Warning: Empty DataFrame, nothing to export.")
        return
    file_path = os.path.join(EXPORT_DIR, filename)
    df.to_excel(file_path, index=False)
    print(f"Data exported to Excel: {file_path}")


if __name__ == "__main__":
    # Simple test example exporting a sample DataFrame
    sample_data = {
        "Month": ["2025-08", "2025-09", "2025-10"],
        "Income": [5000, 5200, 5300],
        "Expenses": [3000, 3100, 3200],
        "Net Savings": [2000, 2100, 2100]
    }
    df = pd.DataFrame(sample_data)

    export_to_csv(df, "monthly_summary.csv")
    export_to_excel(df, "monthly_summary.xlsx")
