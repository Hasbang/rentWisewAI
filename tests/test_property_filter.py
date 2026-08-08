# tests/test_property_filter.py

import unittest
from utils.property_filter import (
    calculate_move_in_cost,
    calculate_remaining_cash,
    is_affordable,
    is_high_risk,
    filter_and_rank_properties,
)


class TestCalculateMoveInCost(unittest.TestCase):
    """Tests for the move-in cost calculation."""

    def test_standard_calculation(self):
        """2 years advance on 36,000 yearly rent = 72,000."""
        result = calculate_move_in_cost(36000, 2)
        self.assertEqual(result, 72000)

    def test_one_year_advance(self):
        """1 year advance on 18,000 yearly rent = 18,000."""
        result = calculate_move_in_cost(18000, 1)
        self.assertEqual(result, 18000)

    def test_zero_advance(self):
        """0 years advance = 0 move-in cost."""
        result = calculate_move_in_cost(36000, 0)
        self.assertEqual(result, 0)


class TestCalculateRemainingCash(unittest.TestCase):
    """Tests for remaining cash after paying move-in cost."""

    def test_standard_remaining(self):
        """80,000 budget minus 72,000 move-in = 8,000 remaining."""
        result = calculate_remaining_cash(80000, 72000)
        self.assertEqual(result, 8000)

    def test_zero_remaining(self):
        """Spending entire budget leaves zero."""
        result = calculate_remaining_cash(50000, 50000)
        self.assertEqual(result, 0)

    def test_large_remaining(self):
        """500,000 budget minus 72,000 move-in = 428,000 remaining."""
        result = calculate_remaining_cash(500000, 72000)
        self.assertEqual(result, 428000)


class TestIsAffordable(unittest.TestCase):
    """Tests for the affordability check."""

    def test_affordable_property(self):
        """Move-in cost below budget is affordable."""
        self.assertTrue(is_affordable(80000, 72000))

    def test_unaffordable_property(self):
        """Move-in cost above budget is not affordable."""
        self.assertFalse(is_affordable(80000, 96000))

    def test_exact_budget_match(self):
        """Move-in cost exactly equal to budget is affordable."""
        self.assertTrue(is_affordable(80000, 80000))

    def test_one_nle_over_budget(self):
        """Move-in cost one NLE over budget is not affordable."""
        self.assertFalse(is_affordable(80000, 80001))


class TestIsHighRisk(unittest.TestCase):
    """Tests for the 10% capital risk flag."""

    def test_clearly_high_risk(self):
        """5,000 remaining on 100,000 budget is high risk."""
        self.assertTrue(is_high_risk(100000, 5000))

    def test_clearly_safe(self):
        """20,000 remaining on 100,000 budget is safe."""
        self.assertFalse(is_high_risk(100000, 20000))

    def test_exact_boundary_is_not_risky(self):
        """Exactly 10% remaining is NOT high risk — rule is strictly less than."""
        self.assertFalse(is_high_risk(100000, 10000))

    def test_one_nle_below_boundary_is_risky(self):
        """One NLE below 10% threshold triggers the flag."""
        self.assertTrue(is_high_risk(100000, 9999))

    def test_zero_remaining_is_high_risk(self):
        """No cash left after move-in is always high risk."""
        self.assertTrue(is_high_risk(80000, 0))


class TestFilterAndRankProperties(unittest.TestCase):
    """Tests for the main filtering and ranking function."""

    def setUp(self):
        """
        setUp runs before every test in this class.
        We define sample properties here so every test
        starts with the same clean data.
        """
        self.sample_properties = [
            {
                "id": "P001",
                "title": "2-Bed Apartment in Wilberforce",
                "location": "Wilberforce, Freetown",
                "yearlyRent": 36000,
                "advanceRequired": 2,
                "bedrooms": 2,
                "bathrooms": 1,
                "propertyType": "apartment",
                "furnished": True,
                "parking": True,
                "waterSupply": "24/7",
                "electricity": "EDSA + Generator",
                "description": "A quiet apartment close to Hill Station.",
            },
            {
                "id": "P002",
                "title": "3-Bed House in Murray Town",
                "location": "Murray Town, Freetown",
                "yearlyRent": 48000,
                "advanceRequired": 2,
                "bedrooms": 3,
                "bathrooms": 2,
                "propertyType": "house",
                "furnished": False,
                "parking": True,
                "waterSupply": "Tanker",
                "electricity": "EDSA",
                "description": "Large family home.",
            },
            {
                "id": "P003",
                "title": "1-Bed Flat in Kissy",
                "location": "Kissy, Freetown",
                "yearlyRent": 18000,
                "advanceRequired": 1,
                "bedrooms": 1,
                "bathrooms": 1,
                "propertyType": "apartment",
                "furnished": False,
                "parking": False,
                "waterSupply": "Tanker",
                "electricity": "EDSA",
                "description": "Budget-friendly flat.",
            },
        ]

        self.requirements = {
            "budget": 80000,
            "location": "Wilberforce",
            "bedrooms": 2,
            "bathrooms": 1,
            "property_type": "apartment",
            "notes": "I want parking.",
        }

    def test_rejects_unaffordable_properties(self):
        """P002 costs 96,000 which exceeds 80,000 budget — must be rejected."""
        result = filter_and_rank_properties(
            self.sample_properties, self.requirements
        )
        rejected_ids = [p["id"] for p in result["rejected"]]
        self.assertIn("P002", rejected_ids)

    def test_rejects_insufficient_bedrooms(self):
        """P003 has 1 bedroom but renter needs 2 — must be rejected."""
        result = filter_and_rank_properties(
            self.sample_properties, self.requirements
        )
        rejected_ids = [p["id"] for p in result["rejected"]]
        self.assertIn("P003", rejected_ids)

    def test_shortlists_affordable_matching_property(self):
        """P001 is affordable and meets bedroom requirement — must be shortlisted."""
        result = filter_and_rank_properties(
            self.sample_properties, self.requirements
        )
        shortlist_ids = [p["id"] for p in result["shortlist"]]
        self.assertIn("P001", shortlist_ids)

    def test_move_in_cost_calculated_correctly(self):
        """P001 move-in cost must be 36,000 x 2 = 72,000."""
        result = filter_and_rank_properties(
            self.sample_properties, self.requirements
        )
        p001 = next(p for p in result["shortlist"] if p["id"] == "P001")
        self.assertEqual(p001["moveInCost"], 72000)

    def test_remaining_cash_calculated_correctly(self):
        """P001 remaining cash must be 80,000 - 72,000 = 8,000."""
        result = filter_and_rank_properties(
            self.sample_properties, self.requirements
        )
        p001 = next(p for p in result["shortlist"] if p["id"] == "P001")
        self.assertEqual(p001["remainingCash"], 8000)

    def test_empty_properties_list(self):
        """Empty properties list returns empty shortlist and rejected list."""
        result = filter_and_rank_properties([], self.requirements)
        self.assertEqual(len(result["shortlist"]), 0)
        self.assertEqual(len(result["rejected"]), 0)

    def test_zero_budget_rejects_all(self):
        """Zero budget means nothing is affordable."""
        requirements = {**self.requirements, "budget": 0}
        result = filter_and_rank_properties(
            self.sample_properties, requirements
        )
        self.assertEqual(len(result["shortlist"]), 0)


if __name__ == "__main__":
    unittest.main()