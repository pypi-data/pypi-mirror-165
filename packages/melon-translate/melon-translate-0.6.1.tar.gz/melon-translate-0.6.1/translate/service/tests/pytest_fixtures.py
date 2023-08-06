import uuid

import pytest


@pytest.fixture
def readiness_provider(provider_to_fixture):
    """Readiness provider fixture."""
    from translate.service.tests.providers import ReadinessCheckProvider

    provider_to_fixture.add_provider(ReadinessCheckProvider)

    yield provider_to_fixture


@pytest.fixture(scope="session")
def language_factory():
    """Language factory fixture."""
    from translate.service.models import Language
    from translate.service.tests.factories import LanguageFactory

    language = LanguageFactory.create()

    obj, _ = Language.objects.get_or_create(lang_info=language.lang_info)
    yield obj
    obj.delete()


@pytest.fixture(
    scope="session",
    params=[
        "general_accept",
        "1another_one",
        "$my_translation",
        "my msgid " "%$#$@@#534",
    ],
)
def translation_key_factory(request):
    """``TranslationKey`` factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    _tk = TranslationKeyFactory.create(
        snake_name=f"{request.param}_{uuid.uuid4().hex}",
        category=Tk.Category.SERVICE,
    )
    obj, _ = Tk.objects.get_or_create(snake_name=_tk.snake_name, category=_tk.category)
    yield obj
    obj.delete()


@pytest.fixture(
    scope="session",
    params=[
        {
            "keys": [
                {
                    "key": "$my_translation",
                    "usage_context": "$my_translation context",
                },
                {
                    "key": "1another_one",
                    "usage_context": "1another_one context",
                },
            ]
        },
    ],
)
def translation_key_with_context_factory(request):
    """``TranslationKey`` that have usage context inserted factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    tks = [
        TranslationKeyFactory.create(
            snake_name=f"{tk.get('key')}_{uuid.uuid4().hex}",
            category=Tk.Category.SERVICE,
            usage_context=tk.get("usage_context"),
        )
        for tk in request.param.get("keys")
    ]

    yield tks

    for tk in tks:
        tk.delete()


@pytest.fixture(
    scope="session",
    params=[
        "snake_name_one",
        "snake_name_two2",
        "snake_name_%$#@%^&@",
    ],
)
def translation_key_mimo_factory(request):
    """``TranslationKey`` with mimo snake_names factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    tk = TranslationKeyFactory.create(
        snake_name=f"{request.param}_{uuid.uuid4().hex}",
        category=Tk.Category.SERVICE,
    )

    yield tk

    tk.delete()


@pytest.fixture(scope="session")
def translation_factory(language_factory, translation_key_factory):
    """Translation factory fixture."""
    from translate.service.tests.factories import TranslationFactory

    obj = TranslationFactory.create(language=language_factory, key=translation_key_factory)

    yield obj, language_factory, translation_key_factory
    obj.delete()


@pytest.fixture(scope="session")
def translation_mimo_factory(language_factory, translation_key_mimo_factory):
    """Translation factory fixture."""
    from translate.service.tests.factories import TranslationFactory

    obj = TranslationFactory.create(language=language_factory, key=translation_key_mimo_factory)

    yield obj, language_factory, translation_key_mimo_factory
    obj.delete()


@pytest.fixture(scope="function")
def translation_provider(provider_to_fixture):

    from translate.service.tests.providers import TranslationProvider

    provider_to_fixture.add_provider(TranslationProvider)

    yield provider_to_fixture


@pytest.fixture(scope="function")
def language_provider(provider_to_fixture):

    from translate.service.tests.providers import LanguageProvider

    provider_to_fixture.add_provider(LanguageProvider)

    yield provider_to_fixture


@pytest.fixture(scope="function")
def translation_key_provider(provider_to_fixture):

    from translate.service.tests.providers import TranslationKeyProvider

    provider_to_fixture.add_provider(TranslationKeyProvider)

    yield provider_to_fixture


@pytest.fixture
def user_account(worker_id):
    """Use a different account in each xdist worker"""
    return f"account_{worker_id}"


@pytest.fixture
def import_translations_fixture():
    """Inserts data into test database before running tests. Needed for ``client`` tests."""
    from django.core.management import call_command

    call_command("import_translations", translations_dir="translate/service/tests/fixtures")
