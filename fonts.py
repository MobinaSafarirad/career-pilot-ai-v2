# Loads custom font files from the fonts/ folder for Persian and English text rendering.

from PySide6.QtGui import QFontDatabase

# List of Persian font file paths to load.
FA_FONT_FILES = [
    "fonts/DigiHamishe/Digi Hamishe Regular.ttf",
    "fonts/DigiHamishe/Digi Hamishe Bold.ttf",
]

# List of English font file paths to load.
EN_FONT_FILES = [
    "fonts/Rubik/Rubik-VariableFont_wght.ttf",
]

# Fallback font names used if the specified font files fail to load.
FA_FALLBACK = "Vazirmatn"
EN_FALLBACK = "Segoe UI"

# Dictionary to store the successfully loaded font family names for each language.
_loaded_family = {"fa": FA_FALLBACK, "en": EN_FALLBACK}


def _load_one(path):
    # Attempt to load a single font file and return its family name.
    # Add the font file to the application's font database.
    font_id = QFontDatabase.addApplicationFont(path)
    # Check if the font loaded successfully.
    if font_id == -1:
        # Print an error message if loading failed.
        print("Could not load font:", path)
        return None
    # Retrieve the font family names associated with the loaded font.
    families = QFontDatabase.applicationFontFamilies(font_id)
    # Return the first family name if available.
    if families:
        return families[0]
    return None


def load_fonts():
    # Load all font files for both Persian and English.
    # This function must be called once, immediately after creating QApplication.
    # Load each Persian font file and update the loaded family if successful.
    for path in FA_FONT_FILES:
        family = _load_one(path)
        if family:
            _loaded_family["fa"] = family
    # Load each English font file and update the loaded family if successful.
    for path in EN_FONT_FILES:
        family = _load_one(path)
        if family:
            _loaded_family["en"] = family


def get_family(lang_code):
    # Return the loaded font family name for a given language code.
    # If the language code is not found, fall back to the English fallback font.
    return _loaded_family.get(lang_code, EN_FALLBACK)