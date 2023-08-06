import django.urls.exceptions
import pytest
import redis
import requests.status_codes
from decouple import config
from django.contrib.staticfiles.testing import LiveServerTestCase


@pytest.mark.client
class TestTranslateClientModel(LiveServerTestCase):
    """Tests for ``TranslateClient`` utils methods."""

    # TODO: Implement lifecycle of functional tests using pytest and not django way.
    #  Mixing those usually comes at the cost.

    def setUp(self):
        """Set's up test data for a test."""
        from django.core.management import call_command

        call_command(
            "import_translations", translations_dir="translate/service/tests/fixtures"
        )

    def test_filter(self):
        """Tests ``filter`` method without additional filters."""
        from melon_translate_client import Client

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)
        language = "de"

        # Requests for German language should return some values.
        german_language_response = c.filter(language, no_cache=True)
        assert (
            german_language_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert german_language_response.json(), "Should have returned some values."

        # Non-existent language should return HTTP status 200 OK, but no translation values.
        incorrect_language_response = c.filter("abcd", no_cache=True)
        assert (
            incorrect_language_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert not incorrect_language_response.json(), "Should have returned no values."

        # No language selected should throw an error for incorrect url path.
        with pytest.raises(django.urls.exceptions.NoReverseMatch):
            _ = c.filter("")

    def test_filter_view_name(self):
        """Tests ``filter`` method with ``view_name`` filter."""
        from melon_translate_client import Client

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)
        language = "de"

        view_response = c.filter(language, views=["translation_center"], no_cache=True)
        assert (
            view_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert view_response.json(), "Should have returned some values."

        no_view_response = c.filter(language, views=["view12", "view21"], no_cache=True)
        assert (
            no_view_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert not no_view_response.json(), "Should have returned no values."

    def test_filter_occurrences(self):
        """Tests ``filter`` method with ``occurrences`` filter."""
        from melon_translate_client import Client

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)
        language = "de"

        occurrences_response = c.filter(
            language,
            occurrences=["new_mdt/apps/mdt_apartments/api/docs.py"],
            no_cache=True,
        )

        assert (
            occurrences_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."

        assert occurrences_response.json(), "Should have returned some values."

        incorrect_occurrences_response = c.filter(
            language, occurrences=["abcd"], no_cache=True
        )
        assert (
            incorrect_occurrences_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert (
            not incorrect_occurrences_response.json()
        ), "Should have returned no values."

    def test_filter_snake_keys(self):
        """Tests ``filter`` method with ``occurrences`` filter."""
        from melon_translate_client import Client

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)
        language = "de"

        snake_keys_response = c.filter(
            language,
            snake_keys=[
                "admin_dossier_downloading",
                "admin_landlord_request",
                "general_conditions",
            ],
            no_cache=True,
        )

        response_json = snake_keys_response.json()

        responses = []
        for i in range(len(response_json)):
            responses.append(response_json[i].get("key").get("snake_name"))

        assert (
            snake_keys_response.status_code == requests.status_codes.codes.ok
        ), "Status code should be 200."
        assert response_json, "Should have returned some values."
        assert len(response_json) == 3, "Should return 3 keys objects"
        assert responses
        assert "admin_dossier_downloading" in responses
        assert "admin_landlord_request" in responses
        assert "general_conditions" in responses

        incorrect_snake_key_response = c.filter(
            language,
            snake_keys=["key_one_that_doesnt_exist", "key_two_that_doesnt_exist"],
            no_cache=True,
        )

        assert (
            incorrect_snake_key_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert (
            not incorrect_snake_key_response.json()
        ), "Should have returned no values."

    def test_response_pagination(self):
        """Test JSON response for different pages."""
        from melon_translate_client import Client

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)
        language = "de"

        first_page_response = c.filter(language, page_size=4, page=1, no_cache=True)
        assert (
            first_page_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert first_page_response.json(), "Should have returned some values."
        assert (
            len(first_page_response.json()) == 4
        ), "Should return same number of records as stated in ``page_size`` parameter."

        # Request results from second page.
        second_page_response = c.filter(language, page_size=4, page=2, no_cache=True)
        assert (
            second_page_response.status_code == requests.status_codes.codes.ok
        ), "Should have returned HTTP status code 200 OK."
        assert (
            first_page_response.json() is not second_page_response.json()
        ), "Should have returned different values from the first page."
        assert (
            len(first_page_response.json()) == 4
        ), "Should return same number of records as stated in ``page_size`` parameter."

    def test_redis_caching_for_filter_method(self):
        """Tests redis caching for filter method with additional filters."""
        from melon_translate_client import Client

        cache = redis.Redis(host="0.0.0.0", port=6379, db=0)
        cache.flushall()

        port = self.live_server_url.split(":")[2]
        c = Client(config("TRANSLATE_ADDRESS", default="http://localhost"), port)

        language = "de"
        _ = c.filter(
            language,
            views=["translation_center"],
        )
        _ = c.filter(
            language,
            occurrences=[
                "new_mdt/apps/mdt_apartments/api/docs.py",
            ],
        )

        maps_no_expire = [
            f"{language}_id_name",
            f"{language}_occurrences",
            f"{language}_snake_name",
            f"{language}_views",
        ]
        for key in maps_no_expire:
            assert cache.hgetall(key), "Should have returned some values."
            assert (
                cache.ttl(key) == -1
            ), "TTL for reverse indexes and values should always be None. We only expire indexes."

        assert c.snake_key(language, "admin_dossier_downloading")
