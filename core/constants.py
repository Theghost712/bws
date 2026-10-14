"""Shared domain constants for the Paveline platform.

Keeping choices in one place means the wish generator, the birthday forms and
the card designer always agree on the same relationship/tone vocabulary, and a
new option only has to be added once.
"""

RELATIONSHIP_WIFE = "wife"
RELATIONSHIP_HUSBAND = "husband"
RELATIONSHIP_GIRLFRIEND = "girlfriend"
RELATIONSHIP_BOYFRIEND = "boyfriend"
RELATIONSHIP_FRIEND = "friend"
RELATIONSHIP_MOTHER = "mother"
RELATIONSHIP_FATHER = "father"
RELATIONSHIP_SISTER = "sister"
RELATIONSHIP_BROTHER = "brother"
RELATIONSHIP_SON = "son"
RELATIONSHIP_DAUGHTER = "daughter"
RELATIONSHIP_RELATIVE = "relative"
RELATIONSHIP_COLLEAGUE = "colleague"
RELATIONSHIP_TEACHER = "teacher"
RELATIONSHIP_OTHER = "other"

RELATIONSHIP_CHOICES = [
    (RELATIONSHIP_WIFE, "Wife"),
    (RELATIONSHIP_HUSBAND, "Husband"),
    (RELATIONSHIP_GIRLFRIEND, "Girlfriend"),
    (RELATIONSHIP_BOYFRIEND, "Boyfriend"),
    (RELATIONSHIP_FRIEND, "Friend"),
    (RELATIONSHIP_MOTHER, "Mother"),
    (RELATIONSHIP_FATHER, "Father"),
    (RELATIONSHIP_SISTER, "Sister"),
    (RELATIONSHIP_BROTHER, "Brother"),
    (RELATIONSHIP_SON, "Son"),
    (RELATIONSHIP_DAUGHTER, "Daughter"),
    (RELATIONSHIP_RELATIVE, "Relative"),
    (RELATIONSHIP_COLLEAGUE, "Colleague"),
    (RELATIONSHIP_TEACHER, "Teacher"),
    (RELATIONSHIP_OTHER, "Other"),
]

TONE_ROMANTIC = "romantic"
TONE_EMOTIONAL = "emotional"
TONE_FUNNY = "funny"
TONE_INSPIRATIONAL = "inspirational"
TONE_RELIGIOUS = "religious"
TONE_SHORT = "short"
TONE_HEARTFELT = "heartfelt"
TONE_FORMAL = "formal"
TONE_CREATIVE = "creative"

TONE_CHOICES = [
    (TONE_ROMANTIC, "Romantic"),
    (TONE_EMOTIONAL, "Emotional"),
    (TONE_FUNNY, "Funny"),
    (TONE_INSPIRATIONAL, "Inspirational"),
    (TONE_RELIGIOUS, "Religious"),
    (TONE_SHORT, "Short and sweet"),
    (TONE_HEARTFELT, "Heartfelt"),
    (TONE_FORMAL, "Formal"),
    (TONE_CREATIVE, "Creative"),
]

LENGTH_SHORT = "short"
LENGTH_MEDIUM = "medium"
LENGTH_LONG = "long"

LENGTH_CHOICES = [
    (LENGTH_SHORT, "Short"),
    (LENGTH_MEDIUM, "Medium"),
    (LENGTH_LONG, "Long"),
]

# Language codes paired with their display name and text direction. Adding a
# language here (plus a message catalogue in wishes/messages) is all that is
# required to offer it in the interface.
SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English", "dir": "ltr"},
    {"code": "sw", "name": "Kiswahili", "dir": "ltr"},
    {"code": "fr", "name": "Français", "dir": "ltr"},
    {"code": "es", "name": "Español", "dir": "ltr"},
    {"code": "ar", "name": "العربية", "dir": "rtl"},
]

LANGUAGE_CODES = [language["code"] for language in SUPPORTED_LANGUAGES]

RTL_LANGUAGES = [language["code"] for language in SUPPORTED_LANGUAGES if language["dir"] == "rtl"]

REMINDER_ON_DAY = 0
REMINDER_ONE_DAY = 1
REMINDER_THREE_DAYS = 3
REMINDER_SEVEN_DAYS = 7

REMINDER_OFFSET_CHOICES = [
    (REMINDER_ON_DAY, "On the birthday"),
    (REMINDER_ONE_DAY, "One day before"),
    (REMINDER_THREE_DAYS, "Three days before"),
    (REMINDER_SEVEN_DAYS, "Seven days before"),
]

# Card template categories mirror the wish tones so the gallery can be
# filtered consistently with the generator.
CARD_CATEGORY_CHOICES = [
    ("romantic", "Romantic"),
    ("floral", "Floral"),
    ("colorful", "Colorful celebration"),
    ("elegant", "Elegant"),
    ("minimalist", "Minimalist"),
    ("children", "Children's birthday"),
    ("religious", "Religious"),
    ("professional", "Professional"),
]

ORIENTATION_CHOICES = [
    ("landscape", "Landscape"),
    ("portrait", "Portrait"),
]
