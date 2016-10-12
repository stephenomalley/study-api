import unittest

import mock
from flask import json
from studies_api.fields.study import study_fields


class TestApiMixin(object):

    def setUp(self):
        # os.environ["MONGOHQ_URL"] = "mongodb://localhost:27017/test"
        from studies_api import app as studies_api
        self.app = studies_api.test_client()

    def tearDown(self):
        pass

    def get_mock_studies(self):
        return [
            self.get_mock_study()
        ]

    def get_mock_study(self):
        return {
            "id": "849d3889vds0345",
            "name": "Test Study",
            "available_places": 30,
            "user": "2"
        }

class TestStudyApiPost(TestApiMixin, unittest.TestCase):

    def test_returns_status_created(self):
        response = self.app.post("/api/v1/studies", data=self._get_mock_study_post())
        self.assertEqual(201, response.status_code, "The status returned was not 201 Created")

    def test_returns_created_object(self):
        content, data = self._generate_post_content()
        self.assertIn("id", content.keys(), "The jey id was not found in the returned object")

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_returns_created_object_values_are_correct(self, mock_study):
        mock_study.return_value = self.get_mock_study()
        content, data = self._generate_post_content()
        for key, value in data.iteritems():
            self.assertEquals(
                value,
                content[key],
                "The value expected for entry {entry} did not equal [ {val} != {res}]".format(entry=key, val=value, res=content[key])
            )

    def test_id_is_generated_on_created_object(self):
        content, data = self._generate_post_content()
        self.assertIsNotNone(content["id"], "The id returned was None")

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_save_to_database_is_made(self, mock_save):
        data = self._get_mock_study_post()
        data["_id"] = "mock3r4lue"
        mock_save.return_value = data
        content, post_data = self._generate_post_content()
        mock_save.assert_called_once_with(post_data)

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_after_save_id_is_returned_in_response_and_is_not_none(self, mock_save):
        data = self._get_mock_study_post()
        data["_id"] = "mock3r4lue"
        mock_save.return_value = data
        content, post_data = self._generate_post_content()
        self.assertEqual(content["id"], data["_id"], "The id returned was not the expected id")

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_posting_with_available_places_as_string_returns_bad_request(self, mock_save):
        response = self.app.post("/api/v1/studies", data={"available_places": "henenkjk"})
        self.assertEqual(400, response.status_code, "A bad request was not made despite passing available_places a string")
        self.assertEqual(0, mock_save.call_count, "The save method was called meaning available places excepts a string")

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_posting_with_available_places_as_string_returns_error_message(self, mock_save):
        response = self.app.post("/api/v1/studies", data={"available_places": "henenkjk"})
        content = json.loads(response.data)
        self.assertIn("message", content, "key message not found in error json")


    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_posting_with_available_places_error_message_contains_error_info(self, mock_save):
        response = self.app.post("/api/v1/studies", data={"available_places": "henenkjk", "name": "help", "user": "87hy"})
        content = json.loads(response.data)
        self.assertEqual(
            "The number of places available on the study.",
            content["message"]["available_places"],
            "The returned error message was different to that expected."
        )

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_posting_without_study_name_results_in_error_message(self, mock_save):
        response = self.app.post("/api/v1/studies", data={"available_places": "henenkjk", "user": "87hy"})
        content = json.loads(response.data)
        self.assertEqual(
            "The name of the Study. Should not be blank.",
            content["message"]["name"],
            "The returned error message was different to that expected."
        )

    @mock.patch("studies_api.resources.api.v1.study.save_study")
    def test_posting_without_user_results_in_error_message(self, mock_save):
        response = self.app.post("/api/v1/studies", data={"available_places": "henenkjk", "name": "help"})
        content = json.loads(response.data)
        self.assertEqual(
            "The ObjectId of the user that created the study.",
            content["message"]["user"],
            "The returned error message was different to that expected."
        )

    def test_returns_bad_request_due_to_additional_data(self):
        response = self.app.post("/api/v1/studies", data=self.get_mock_study())
        self.assertEqual(400, response.status_code, "The request was valid even although it shouldn't have been")

    def _generate_post_content(self):
        data = self._get_mock_study_post()
        response = self.app.post("/api/v1/studies", data=data)
        return json.loads(response.data), data

    def _get_mock_study_post(self):
        data = self.get_mock_study()
        del data["id"]
        return data


class TestStudyApiGet(TestApiMixin, unittest.TestCase):
    def test_returns_status_ok(self):
        response = self.app.get("/api/v1/studies/57fd369e39a63df2114a6847")
        self.assertEqual(200, response.status_code, "Requests to a single study returns successful response")

    def test_returns_json(self):
        response = self.app.get("/api/v1/studies/57fd369e39a63df2114a6847")
        content = json.loads(response.data)
        self.assertTrue(isinstance(content, dict), "Response returns a json object")

    def test_response_json_not_empty(self):
        response = self.app.get("/api/v1/studies/57fd369e39a63df2114a6847")
        content = json.loads(response.data)
        self.assertNotEqual({}, content, "Response body is not empty")

    def test_response_contains_correct_fields(self):
        response = self.app.get("/api/v1/studies/57fd369e39a63df2114a6847")
        content = json.loads(response.data)
        for field in study_fields:
            self.assertIn(field, content)

    @mock.patch("studies_api.resources.api.v1.study.get_study_by_id")
    def test_response_body_has_correct_object(self, mock_study):
        mock_study.return_value = self.get_mock_study()
        response = self.app.get("/api/v1/studies/57fd369e39a63df2114a6847")
        content = json.loads(response.data)
        self.assertEqual(content["name"], "Test Study")
        mock_study.assert_called_once_with("57fd369e39a63df2114a6847")

    def test_request_with_invalid_id_gives_400(self):
        response = self.app.get("/api/v1/studies/1")
        self.assertEqual(400, response.status_code)

    def test_request_with_invalid_id_returns_error_message(self):
        response = self.app.get("/api/v1/studies/1")
        error = json.loads(response.data)
        self.assertIn("message", error)

    def test_request_with_invalid_id_returns_message_with_error_reason(self):
        response = self.app.get("/api/v1/studies/1")
        error = json.loads(response.data)
        self.assertIn("12-byte input or a 24-character hex string", error["message"])

    @mock.patch("studies_api.resources.api.v1.study.get_study_by_id")
    def test_request_for_non_existing_study_returns_404(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/api/v1/studies/57fd369e39a63df2514a6847")
        self.assertEqual(404, response.status_code)
        mock_study.assert_called_once_with("57fd369e39a63df2514a6847")

    @mock.patch("studies_api.resources.api.v1.study.get_study_by_id")
    def test_request_for_non_existing_study_error_response_contains_message(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/api/v1/studies/57fd369e79a63df2114a6847")
        error = json.loads(response.data)
        mock_study.assert_called_once_with("57fd369e79a63df2114a6847")
        self.assertIn("message", error)

    @mock.patch("studies_api.resources.api.v1.study.get_study_by_id")
    def test_request_for_non_existing_study_error_response_is_well_formed(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/api/v1/studies/57fd369b39a63df2114a6847")
        error = json.loads(response.data)
        mock_study.assert_called_once_with("57fd369b39a63df2114a6847")
        self.assertIn("study not found", error["message"].lower())


class TestStudyApiList(TestApiMixin, unittest.TestCase):
    def test_returns_status_ok(self):
        response = self.app.get("/api/v1/studies")
        self.assertEqual(200, response.status_code, "Requests to studies returns successful response")

    def test_end_point_returns_data(self):
        response = self.app.get("/api/v1/studies")
        content = json.loads(response.data)
        self.assertTrue("data" in content)

    def test_end_point_returns_list_of_json(self):
        response = self.app.get("/api/v1/studies")
        content = json.loads(response.data)
        self.assertTrue(isinstance(content["data"], list), "Response data is returned in list format")

    def test_content_returns_ok_without_data(self):
        response = self.app.get("/api/v1/studies")
        data = json.loads(response.data)["data"]
        self.assertEqual(data, [])

    @mock.patch("studies_api.resources.api.v1.study.get_all_studies")
    def test_content_has_item(self, mock_studies):
        mock_studies.return_value = self.get_mock_studies()
        response = self.app.get("/api/v1/studies")
        data = json.loads(response.data)["data"]
        self.assertNotEqual(data, [])
        mock_studies.assert_called_once()

    @mock.patch("studies_api.resources.api.v1.study.get_all_studies")
    def test_content_has_itest_item_in_data_list_is_correct(self, mock_studies):
        mock_studies.return_value = self.get_mock_studies()
        response = self.app.get("/api/v1/studies")
        data = json.loads(response.data)["data"]
        for item in data:
            for field in study_fields.iterkeys():
                self.assertIn(field, item, "Study object should have correct fields")

        mock_studies.assert_called_once_with()

    def test_end_point_returns_links(self):
        response = self.app.get("/api/v1/studies")
        content = json.loads(response.data)
        self.assertTrue("links" in content)

    def test_link_data_is_correct(self):
        response = self.app.get("/api/v1/studies")
        links = json.loads(response.data)["links"]
        self.assertEqual(links, {"self": "http://localhost/api/v1/studies"})


if __name__ == '__main__':
    unittest.main
