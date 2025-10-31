import argparse
import src.cli as cli
import src.database as db

def main():
    parser = argparse.ArgumentParser(description="Advanced Personal Finance Tracker")
    parser.add_argument('--init-db', action='store_true', help='Initialize the database schema')
    parser.add_argument('--cli', action='store_true', help='Start the interactive CLI')
    args = parser.parse_args()

    if args.init_db:
        db.initialize_db()
    elif args.cli:
        cli.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()