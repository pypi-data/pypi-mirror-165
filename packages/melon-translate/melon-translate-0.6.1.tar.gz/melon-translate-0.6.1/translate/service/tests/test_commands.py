import pytest
from django.core.management import call_command


class TestImportCommand:
    @pytest.mark.command
    def test_objects_creation(self, import_translations_fixture):
        """Check importing of translations."""
        from translate.service.models import Language, Translation, TranslationKey

        language = Language.objects.get(lang_info="de")
        record = Translation.objects.filter(translation="Startdatum auf Webseite")
        key_record = TranslationKey.objects.get(snake_name="admin_landlord_request")

        assert language
        assert record
        assert key_record
        assert key_record.snake_name
