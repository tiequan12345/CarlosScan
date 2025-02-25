import argparse
import config_fetcher
import project_fetcher
import project_printer
# import database_storer  # Uncomment if you want to use database storage

def main():
    parser = argparse.ArgumentParser(description="Fetch and display project details.")
    parser.add_argument("project", help="Project ID (e.g., 'em', 'aerodrome')")
    parser.add_argument("wallet", help="Wallet address")
    parser.add_argument("--strategy", default="", help="Strategy name (optional)")
    parser.add_argument("--lp_summary", action="store_true", help="Include LP summary")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel fetching")
    parser.add_argument("--hide_no_rewards", action="store_true", help="Hide pools with no rewards")

    args = parser.parse_args()

    try:
        chain, project = config_fetcher.fetch_configs({
            "project_id": args.project,
            "wallet": args.wallet,
            "strategy": args.strategy,
            "lp_summary": args.lp_summary,
            "parallel": args.parallel,
            "hide_no_rewards": args.hide_no_rewards
        })

        fetched_project = project_fetcher.fetch_all(chain, project, args.wallet, args.strategy)
        project_printer.print_details(fetched_project)

        # Uncomment the following lines if you want to use database storage:
        # database_storer.store(chain, fetched_project)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()