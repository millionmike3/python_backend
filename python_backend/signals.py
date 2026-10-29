from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def compute_property_signal_from_dict(data: dict):
    """
    Simple placeholder scoring engine.
    Replace with real underwriting logic later.
    """

    score = 0
    accelerated = False

    # Example scoring logic
    if data.get("cap_rate"):
        score += data["cap_rate"] * 10

    if data.get("dscr"):
        score += data["dscr"] * 20

    if data.get("noi_value_ratio"):
        score += data["noi_value_ratio"] * 15

    # Example accelerated pass logic
    if data.get("dscr") and data["dscr"] >= 1.25:
        accelerated = True

    status = "PASS" if score >= 50 else "REVIEW"

    return score, status, accelerated


# 🔥 REQUIRED ALIAS FOR YOUR ROUTER
def compute_property_signal(data: dict):
    """
    Alias wrapper so routers expecting compute_property_signal do not break.
    """
    return compute_property_signal_from_dict(data)


def compute_borrower_signal(data: dict):
    """
    Basic borrower-level scoring.
    Replace with full underwriting logic later.
    """

    score = 0

    # Credit score contribution
    if data.get("credit_score"):
        score += data["credit_score"] / 10  # 700 → 70 points

    # DTI contribution (lower is better)
    if data.get("dti") is not None:
        score += max(0, 50 - data["dti"])  # DTI 30 → +20 points

    # Income stability
    if data.get("income_stability_years"):
        score += data["income_stability_years"] * 5

    # Employment type
    if data.get("employment_type") == "W2":
        score += 15
    elif data.get("employment_type") == "1099":
        score += 5

    status = "PASS" if score >= 60 else "REVIEW"

    return score, status


def compute_ultra_favorable_signal(data: dict):
    """
    Detect ultra-favorable borrower conditions.
    Used for accelerated approvals or premium pricing.
    """

    favorable = False

    credit = data.get("credit_score", 0)
    dti = data.get("dti", 100)
    reserves = data.get("cash_reserves_months", 0)

    if credit >= 760 and dti <= 30 and reserves >= 6:
        favorable = True

    return favorable
