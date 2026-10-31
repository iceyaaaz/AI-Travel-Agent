def main(
    new_city: str,
    new_days: float,
    new_preferences: str,
    new_start_date: str,
    old_city: str,
    old_days: float,
    old_preferences: str,
    old_start_date: str
) -> dict:

    def clean(value):
        return str(value or "").strip()

    def days_number(value):
        try:
            number = float(value or 0)
            if number > 0 and number.is_integer():
                return int(number)
        except (TypeError, ValueError):
            pass
        return 0

    city = clean(new_city) or clean(old_city)
    days = days_number(new_days) or days_number(old_days)
    start_date = clean(new_start_date) or clean(old_start_date)

    previous = clean(old_preferences)
    incoming = clean(new_preferences)

    if previous and incoming and incoming != previous:
        preferences = previous + "；" + incoming
    else:
        preferences = incoming or previous


    return {
        "city": city,
        "days": days,
        "preferences": preferences,
        "start_date": start_date,
        "pending_intent": "trip"
    }
