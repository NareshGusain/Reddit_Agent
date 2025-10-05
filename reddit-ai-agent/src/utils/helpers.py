def log_message(message: str) -> None:
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(message)

def format_pain_points(pain_points: list) -> str:
    return "\n".join(f"- {point}" for point in pain_points)