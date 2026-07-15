from core.scraper import scrape
from enrichment.enrich import process_all_businesses
from reporting.excel import export_to_excel
from db.ops import (
    get_all_businesses,
    get_raw_businesses,
    delete_all_businesses
)
from db.db import init_db
from colorama import init, Fore
import os, time
init(autoreset=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("=" * 74)
    print("      REAL ESTATE INTELLIGENCE SYSTEM(A DEMO FOR REEVES REAL ESTATE)")
    print("=" * 74)


def print_menu():
    print()
    print("1. Scrape Google Maps")
    print("2. Enrich Existing Businesses")
    print("3. Generate Excel Report")
    print("4. Run Full Pipeline")
    print("5. Database Statistics")
    print("6. Clear Database")
    print("0. Exit")
    print()


def scrape_menu():
    clear_screen()
    query = input("Search query: ").strip()
    try:
        max_results = int(input("number of businesses : "))
    except ValueError:
        print(Fore.RED + "Invalid number.")

        return
    print(Fore.YELLOW + "\nScraping Google Maps...\n")
    scrape(query, max_results)
    print(Fore.GREEN + "✓ Scraping finished.")


def enrich_menu():
    clear_screen()
    print(Fore.YELLOW + "\nEnriching businesses...\n")
    businesses = get_raw_businesses()
    process_all_businesses(businesses)
    print(Fore.GREEN + "✓ Enrichment finished.")


def report_menu():
    clear_screen()
    businesses = get_all_businesses()

    if not businesses:
        print(Fore.RED + "Database is empty.")
        return
    filename = input("Enter the name of the file: ")
    export_to_excel(businesses, filename = filename + ".xlsx")

    print(Fore.GREEN + "✓ report.xlsx generated.")


def full_pipeline():
    clear_screen()
    query = input("Search query: ").strip()

    try:
        max_results = int(input("number of businesses : "))
    except ValueError:
        print(Fore.RED + "Invalid number.")
        return

    print(Fore.YELLOW + "\n[1/3] Scraping...")
    scrape(query, max_results)
    print(Fore.YELLOW + "[2/3] Enriching...")
    businesses = get_raw_businesses()
    process_all_businesses(businesses)

    print(Fore.YELLOW + "[3/3] Generating report...")
    businesses = get_all_businesses()
    if not businesses:
        print(Fore.RED + "Database is empty.")
        return
    filename = input("Enter the name of the file: ")
    export_to_excel(businesses, filename = filename + ".xlsx")

    print(Fore.GREEN)
    print("=" * 50)
    print("✓ FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 50)


def stats_menu():
    clear_screen()
    businesses = get_all_businesses()

    if not businesses:
        print(Fore.RED + "Database is empty.")
        return

    total = len(businesses)

    enriched = sum(
        b.status == "enriched"
        for b in businesses
    )

    with_website = sum(
        bool(b.website)
        for b in businesses
    )

    with_email = sum(
        len(b.emails) > 0
        for b in businesses
    )

    with_linkedin = sum(
        bool(b.linkedin)
        for b in businesses
    )

    with_facebook = sum(
        bool(b.facebook)
        for b in businesses
    )

    with_instagram = sum(
        bool(b.instagram)
        for b in businesses
    )
    with_youtube = sum(
        bool(b.youtube)
        for b in businesses
    )

    avg_score = round(
        sum(
            b.lead_score or 0
            for b in businesses
        ) / total,
        2
    )

    print()
    print("=" * 40)
    print("DATABASE STATISTICS")
    print("=" * 40)

    print(f"Businesses          : {total}")
    print(f"Enriched            : {enriched}")
    print(f"With Website        : {with_website}")
    print(f"With Email          : {with_email}")
    print(f"With LinkedIn       : {with_linkedin}")
    print(f"With Facebook       : {with_facebook}")
    print(f"With Instagram       : {with_instagram}")
    print(f"With Youtube       : {with_youtube}")
    print(f"Average Lead Score  : {avg_score}")


def clear_database_menu():
    clear_screen()
    print(Fore.RED)
    confirm = input(
        "Delete ALL businesses? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    delete_all_businesses()

    print(Fore.GREEN + "Database cleared.")


def main():

    init_db()

    while True:
        clear_screen()
        print_banner()
        print_menu()

        choice = input("Choice > ").strip()

        if choice == "1":
            scrape_menu()

        elif choice == "2":
            enrich_menu()

        elif choice == "3":
            report_menu()

        elif choice == "4":
            full_pipeline()

        elif choice == "5":
            stats_menu()

        elif choice == "6":
            clear_database_menu()

        elif choice == "0":
            print(Fore.CYAN + "Goodbye.")
            time.sleep(0.5)
            break

        else:
            print(Fore.RED + "Invalid choice.")

        input("\nPress ENTER to continue...")


if __name__ == "__main__":
    main()