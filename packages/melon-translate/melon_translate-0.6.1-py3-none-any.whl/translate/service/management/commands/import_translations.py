import glob
import json
import operator
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

import django.db.utils
import polib
from django.conf import settings
from django.conf.locale import LANG_INFO
from django.core.management.base import BaseCommand

from translate.core.utils.logging import log
from translate.service.models import Language, Translation, TranslationKey

SNAKE_TRANSLATIONS = Path("snake_translations.json")
# DEFAULT_DIR_PATH = Path("translate/service/tests/fixtures")  # This is a testing directory
DEFAULT_DIR_PATH = Path("export_translations")


def extract_language(path: str) -> str:
    """Extract language from path with locale."""
    parts = path.split("/")
    idx = parts.index("locale")
    return parts[idx + 1]


class Command(BaseCommand):
    help = "Importing translation keys command from .json and .po files"

    def add_arguments(self, parser):
        """Attach argument for import_translations command."""
        parser.add_argument(
            "translations_dir",
            type=str,
            nargs="?",
            default=DEFAULT_DIR_PATH,
        )

    @staticmethod
    def read_po_files(dirs) -> dict:
        """Read po files."""
        log.info("Reading po files.")
        po_files = {
            po_file: polib.pofile(po_file, encoding="utf-8")
            for po_file in glob.iglob(f"{dirs}/**/*.po", recursive=True)
        }

        files_with_languages = defaultdict(list)
        for file_path, file in po_files.items():
            lang = extract_language(file_path)
            files_with_languages[lang].append((file_path, file))

        log.info("Done")
        return files_with_languages

    @staticmethod
    def create_po_keys(file_path, file_entries):
        """Create po keys."""
        entries = [
            TranslationKey(
                id_name=entry.msgid,
                id_name_plural=entry.msgid_plural,
                encoding=entry.encoding,
                usage_context=entry.msgctxt,
                occurrences=sorted(map(operator.itemgetter(0), entry.occurrences)),
                flags=entry.flags,
            )
            for entry in file_entries
        ]
        log.info(f"Created and prepared {len(entries)} po TranslationKeys")
        return entries

    @staticmethod
    def create_po_translations(file_path, file_entries, key_entries, language):
        """Import po translations."""
        entries = [
            Translation(
                language=language,
                key=key_entries[idx],
                translation=entry.msgstr if entry.msgstr else entry.msgid,
                translation_plural=entry.msgid_plural,
            )
            for idx, entry in enumerate(file_entries)
        ]
        log.info(f"Created and prepared {len(entries)} po Translations")
        return entries

    @staticmethod
    def process_po_files(dirs):
        """Process po files."""
        po_files = Command.read_po_files(dirs)

        keys, translations = [], []
        for lang, files in sorted(po_files.items()):
            language = Language.objects.get(lang_info=lang)
            for file_path, file_entries in files:
                key_entries = Command.create_po_keys(file_path, file_entries)
                translations += Command.create_po_translations(file_path, file_entries, key_entries, language)
                keys += key_entries

        uniq = {}
        for key in keys:
            if key.id_name in uniq.keys():
                log.info(f"Duplicate ID name {key.id_name}")
            else:
                uniq[key.id_name] = key
        keys = list(uniq.values())

        log.info(f"Prepared {len(keys)} of TranslationKeys via po files. Inserting bulk.")
        inserts = TranslationKey.objects.bulk_create(keys, ignore_conflicts=True)
        log.info(f"Done. Inserted {len(inserts)} po Keys.")

        if len(inserts) != len(keys):
            log.info("WARNING! Some keys were not inserted.")

        log.info(f"Prepared {len(translations)} of Translations via po files. Inserting bulk.")
        translation_inserts = []
        for obj in translations:
            if obj.translation in uniq.keys():
                try:
                    obj.save()
                    translation_inserts.append(obj)
                except django.db.utils.IntegrityError:
                    log.info(
                        f"There was an Integrity Error with {obj.translation} translation and it was not inserted."
                    )
        log.info(f"Done. Inserted {len(translation_inserts)} po Translations.")

    @staticmethod
    def create_json_keys(language_data):
        """Create language data."""
        log.info("Preparing translation keys.")
        keys = [
            TranslationKey(
                snake_name=snake_name, id_name=obj.get("translations"), views=[source_dict] + obj.get("source")
            )
            for source_dict, value in language_data.items()
            for snake_name, obj in value.items()
        ]
        log.info(f"Prepared {len(keys)} translations keys. Inserting in bulk.")
        TranslationKey.objects.bulk_create(keys, ignore_conflicts=True)
        log.info(f"Imported {len(keys)} keys.")
        return keys

    @staticmethod
    def read_json_translations(dirs):
        """Read JSON translations."""
        log.info("Reading json translations")
        translations = json.loads((settings.BASE_DIR.parent / dirs / SNAKE_TRANSLATIONS).read_text())
        log.info("Done")
        return translations

    @staticmethod
    def create_json_translations(translations: Dict[str, Any], lang_key: str):
        """Import snake_names for a specific language."""
        log.info(f"Processing snake_names from JSON translations for {lang_key}")
        language = Language.objects.get(lang_info=lang_key)
        lang_data = translations.get(lang_key)

        bulk_translations = []
        for dict_key, dict_data in lang_data.items():
            keys = {key.snake_name: key for key in TranslationKey.objects.filter(snake_name__in=list(dict_data.keys()))}

            for snake_key, snake_data in dict_data.items():
                translation_key = keys.get(snake_key)
                translation = Translation(
                    language=language,
                    key=translation_key,
                    translation=snake_data.get("translations"),
                    translation_plural=snake_data.get("translations"),
                )
                bulk_translations.append(translation)

        log.info(f"Inserting translations: {len(bulk_translations)}")

        try:
            Translation.objects.bulk_create(bulk_translations, ignore_conflicts=True)
        except django.db.utils.IntegrityError:
            log.info("There was a Integrity Error with json files, none were inserted.")
        log.info("Done")

    @staticmethod
    def process_json_files(dirs):
        """Process json files."""
        translations = Command.read_json_translations(dirs)

        _ = {
            lang: Language.objects.get_or_create(lang_info=lang)
            for lang in translations
            if lang in list(LANG_INFO.keys())
        }

        for lang in translations:
            _ = Command.create_json_keys(translations.get(lang))
            _ = Command.create_json_translations(translations, lang)

    def handle(self, *args, **options):
        """Entrypoint to the command."""

        dir_name = Path(settings.BASE_DIR.parent, options.get("translations_dir"))

        Command.process_json_files(dir_name)
        Command.process_po_files(dir_name)
