def calculate_move_in_cost(yearly_rent, advance_required):
    """
    Calculate the total upfront cost to move into a property.
    Move-in Cost = Yearly Rent × Advance Required

    """

    return yearly_rent * advance_required


def calculate_remaining_cash(budget, move_in_cost):
    """
    Calculate how much cash the renter has left after paying move-in cost.
    """
    return budget - move_in_cost


def is_affordable(budget, move_in_cost):
    """
    Return True if the renter can afford the move-in cost.
    """
    return move_in_cost <= budget


def is_high_risk(budget, remaining_cash):
    """
    Return True if remaining cash is less than 10% of original budget.
    This means the renter is left financially vulnerable after moving in.
    """
    return remaining_cash < (budget * 0.10)


def filter_and_rank_properties(properties, requirements):
    """
    The main filtering function. Takes the full property list and
    renter requirements, returns two lists:
    - shortlist: affordable properties with calculated fields, ranked by match
    - rejected: properties that failed affordability or bedroom check

    Args:
        properties: list of property dicts from data_loader
        requirements: dict of renter requirements from the form

    Returns:
        dict with keys 'shortlist' and 'rejected'
    """
    budget = requirements["budget"]
    needed_bedrooms = requirements["bedrooms"]
    needed_bathrooms = requirements["bathrooms"]
    preferred_type = requirements["property_type"]
    preferred_location = requirements["location"].lower()

    shortlist = []
    rejected = []

    for prop in properties:
        move_in_cost = calculate_move_in_cost(
            prop["yearlyRent"],
            prop["advanceRequired"]
        )
        remaining_cash = calculate_remaining_cash(budget, move_in_cost)

        # ── STEP 1: AFFORDABILITY CHECK ──────────────────────────────
        if not is_affordable(budget, move_in_cost):
            rejected.append({
                **prop,
                "moveInCost": move_in_cost,
                "rejectionReason": (
                    f"Move-in cost of NLE {move_in_cost:,} exceeds "
                    f"budget of NLE {budget:,}"
                )
            })
            continue

        # ── STEP 2: BEDROOM CHECK ────────────────────────────────────
        if prop["bedrooms"] < needed_bedrooms:
            rejected.append({
                **prop,
                "moveInCost": move_in_cost,
                "rejectionReason": (
                    f"Only {prop['bedrooms']} bedroom(s) available, "
                    f"renter needs {needed_bedrooms}"
                )
            })
            continue

        # ── STEP 3: CALCULATE RISK FLAG ──────────────────────────────
        high_risk = is_high_risk(budget, remaining_cash)

        # ── STEP 4: CALCULATE MATCH SCORE ────────────────────────────
        # Score starts at 0. Higher = better match.
        score = 0

        # Location match (most important)
        if preferred_location in prop["location"].lower():
            score += 40

        # Property type match
        if preferred_type != "any":
            if prop["propertyType"] == preferred_type:
                score += 20

        # Bathroom match
        if prop["bathrooms"] >= needed_bathrooms:
            score += 15

        # Bedroom exact match (bonus for exact, not just minimum)
        if prop["bedrooms"] == needed_bedrooms:
            score += 15

        # Amenity bonuses
        if prop.get("parking"):
            score += 5
        if prop.get("furnished"):
            score += 5

        shortlist.append({
            **prop,
            "moveInCost": move_in_cost,
            "remainingCash": remaining_cash,
            "highRisk": high_risk,
            "matchScore": score,
        })

    # Sort shortlist by match score — highest first
    shortlist.sort(key=lambda x: x["matchScore"], reverse=True)

    return {
        "shortlist": shortlist,
        "rejected": rejected,
    }


