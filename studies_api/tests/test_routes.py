import unittest

import mock
from flask import json
from studies_api.fields.study import study_fields


class TestApiMixin(object):
    def setUp(self):
        # os.environ["MONGOHQ_URL"] = "mongodb://localhost:27017/test"
        from studies_api.app import app as studies_api
        self.app = studies_api.test_client()

    def tearDown(self):
        pass

    def get_mock_studies(self):
        return [
            self.get_mock_study()
        ]

    def get_mock_study(self):
        return {
            "id": "84938890345",
            "name": "Test Study",
            "available_places": 30,
            "user": 2
        }


class TestStudyApiGet(TestApiMixin, unittest.TestCase):
    def test_returns_status_ok(self):
        response = self.app.get("/studies/1")
        self.assertEqual(200, response.status_code, "Requests to a single study returns successful response")

    def test_returns_json(self):
        response = self.app.get("/studies/1")
        content = json.loads(response.data)
        self.assertTrue(isinstance(content, dict), "Response returns a json object")

    def test_response_json_not_empty(self):
        response = self.app.get("/studies/1")
        content = json.loads(response.data)
        self.assertNotEqual({}, content, "Response body is not empty")

    def test_response_contains_correct_fields(self):
        response = self.app.get("/studies/1")
        content = json.loads(response.data)
        for field in study_fields:
            self.assertIn(field, content)

    @mock.patch("studies_api.resources.study.get_study_by_id")
    def test_response_body_has_correct_object(self, mock_study):
        mock_study.return_value = self.get_mock_study()
        response = self.app.get("/studies/1")
        content = json.loads(response.data)
        self.assertEqual(content["name"], "Test Study")
        mock_study.assert_called_once_with(1)

    def test_request_with_invalid_id_gives_404(self):
        response = self.app.get("/studies/meeep")
        self.assertEqual(404, response.status_code)

    @mock.patch("studies_api.resources.study.get_study_by_id")
    def test_request_for_non_existing_study_returns_404(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/studies/2")
        self.assertEqual(404, response.status_code)
        mock_study.assert_called_once_with(2)

    @mock.patch("studies_api.resources.study.get_study_by_id")
    def test_request_for_non_existing_study_error_response_contains_message(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/studies/2")
        error = json.loads(response.data)
        mock_study.assert_called_once_with(2)
        self.assertIn("message", error)

    @mock.patch("studies_api.resources.study.get_study_by_id")
    def test_request_for_non_existing_study_error_response_is_well_formed(self, mock_study):
        mock_study.return_value = None
        response = self.app.get("/studies/2")
        error = json.loads(response.data)
        mock_study.assert_called_once_with(2)
        self.assertIn("study not found", error["message"].lower())


class TestStudyApiList(TestApiMixin, unittest.TestCase):
    def test_returns_status_ok(self):
        response = self.app.get("/studies")
        self.assertEqual(200, response.status_code, "Requests to studies returns successful response")

    def test_end_point_returns_data(self):
        response = self.app.get("/studies")
        content = json.loads(response.data)
        self.assertTrue("data" in content)

    def test_end_point_returns_list_of_json(self):
        response = self.app.get("/studies")
        content = json.loads(response.data)
        self.assertTrue(isinstance(content["data"], list), "Response data is returned in list format")

    def test_content_returns_ok_without_data(self):
        response = self.app.get("/studies")
        data = json.loads(response.data)["data"]
        self.assertEqual(data, [])

    @mock.patch("studies_api.resources.study.get_all_studies")
    def test_content_has_item(self, mock_studies):
        mock_studies.return_value = self.get_mock_studies()
        response = self.app.get("/studies")
        data = json.loads(response.data)["data"]
        self.assertNotEqual(data, [])
        mock_studies.assert_called_once()

    @mock.patch("studies_api.resources.study.get_all_studies")
    def test_content_has_itest_item_in_data_list_is_correct(self, mock_studies):
        mock_studies.return_value = self.get_mock_studies()
        response = self.app.get("/studies")
        data = json.loads(response.data)["data"]
        for item in data:
            for field in study_fields.iterkeys():
                self.assertIn(field, item, "Study object should have correct fields")

        mock_studies.assert_called_once_with()

    def test_end_point_returns_links(self):
        response = self.app.get("/studies")
        content = json.loads(response.data)
        self.assertTrue("links" in content)

    def test_link_data_is_correct(self):
        response = self.app.get("/studies")
        links = json.loads(response.data)["links"]
        self.assertEqual(links, {"self": "http://localhost/studies"})


if __name__ == '__main__':
    unittest.main
