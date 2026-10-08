# Manages application language switching between English and Persian.

import json

# List of supported language codes.
LANGUAGES = ["en", "fa"]


class LocaleManager:
    def __init__(self, default_lang="fa"):
        # Set the current language to the default value.
        self.current_lang = default_lang
        # Initialize an empty dictionary to store all language texts.
        self.texts = {}
        # Load translation files for each supported language.
        for lang in LANGUAGES:
            # Build the file path for the language JSON file.
            path = "translation/" + lang + ".json"
            # Open and load the JSON data.
            with open(path, "r", encoding="utf-8") as f:
                self.texts[lang] = json.load(f)

    def set_language(self, lang):
        # Update the current language to the specified one.
        self.current_lang = lang

    def is_rtl(self):
        # Return True if the current language uses Right-to-Left text direction.
        return self.texts[self.current_lang]["direction"] == "rtl"

    def font_family(self):
        # Return the font family name for the current language.
        return self.texts[self.current_lang]["font_family"]

    def tr(self, key):
        # Retrieve a UI text string by its key, falling back to the key itself if not found.
        if key in self.texts[self.current_lang]:
            return self.texts[self.current_lang][key]
        return key

    def skill_label(self, skill_key):
        # Retrieve the translated label for a specific skill.
        return self.texts[self.current_lang]["skill_labels"][skill_key]

    def category_label(self, category_key):
        # Retrieve the translated label for a specific job category.
        return self.texts[self.current_lang]["category_labels"][category_key]

    def salary_label(self, salary_key):
        # Retrieve the translated label for a specific salary level.
        return self.texts[self.current_lang]["salary_labels"][salary_key]

    def job_text(self, job, field):
        # Get a bilingual field (e.g., title, description) from a job object in the current language.
        return job[field][self.current_lang]