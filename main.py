# main.py

from crew.rentwise_crew import run_rentwise_crew

def main():
    # Test requirements — a renter with NLE 80,000
    requirements = {
        "budget": 80000,
        "location": "Hill Station",
        "bedrooms": 2,
        "bathrooms": 1,
        "property_type": "apartment",
        "notes": "I want somewhere quiet with parking. I work at Hill Station.",
    }

    print("\n" + "=" * 60)
    print("   RENTWISE AI — Running Analysis")
    print("=" * 60 + "\n")

    result = run_rentwise_crew(requirements)

    print("\n" + "=" * 60)
    print("   FINAL ADVISORY REPORT")
    print("=" * 60)
    print(result)

if __name__ == "__main__":
    main()