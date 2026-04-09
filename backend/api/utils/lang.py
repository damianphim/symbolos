"""Shared language instruction helper used by chat.py and cards.py."""


def lang_instruction(language: str) -> str:
    """
    Returns a CRITICAL-level language instruction appended last in the system
    prompt so it overrides any language drift caused by English course data.
    """
    if language == "fr":
        return (
            "\n\nCRITICAL LANGUAGE RULE: You MUST respond entirely in French. "
            "Every part of your response — advice, explanations, lists, follow-up questions — "
            "must be in French. Do not switch to English under any circumstance, even if the "
            "student's course titles, grades, or calendar events are in English. "
            "Course codes (e.g. COMP 202) and proper nouns (McGill, Minerva) may stay as-is."
        )
    if language == "zh":
        return (
            "\n\nCRITICAL LANGUAGE RULE: You MUST respond entirely in Simplified Chinese (Mandarin). "
            "Every part of your response must be in Chinese. Do not switch to English under any "
            "circumstance, even if the student's course names, grades, or calendar events are in English. "
            "Course codes (e.g. COMP 202) and proper nouns (McGill, Minerva) may stay as-is."
        )
    return (
        "\n\nCRITICAL LANGUAGE RULE: You MUST respond entirely in English. "
        "Do not use French, Chinese, or any other language in your response, "
        "even if the student's course names, calendar events, or profile data are in another language."
    )
