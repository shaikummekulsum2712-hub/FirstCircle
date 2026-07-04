ALLOWED_COLLEGE_DOMAINS = [
    "college.edu",
    "university.ac.in",
    "student.edu",
    "gmail.com",  # MVP only. Remove this later for real college verification.
]


def extract_email_domain(email: str) -> str:
    if "@" not in email:
        return ""

    return email.split("@")[-1].strip().lower()


def is_allowed_college_email(email: str) -> bool:
    domain = extract_email_domain(email)
    return domain in ALLOWED_COLLEGE_DOMAINS


def is_valid_roll_number(roll_number: str) -> bool:
    cleaned = roll_number.strip()

    if len(cleaned) < 4:
        return False

    return cleaned.replace("-", "").replace("_", "").isalnum()


def list_to_csv(values: list[str]) -> str:
    return ",".join(item.strip() for item in values if item.strip())


def csv_to_list(value: str) -> list[str]:
    if not value:
        return []

    return [item.strip() for item in value.split(",") if item.strip()]