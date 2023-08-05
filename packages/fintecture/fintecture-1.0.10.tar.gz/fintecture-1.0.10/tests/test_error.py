# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from fintecture import six, error


class FintectureError(object):
    def test_formatting(self):
        err = error.FintectureError(u"öre")
        assert six.text_type(err) == u"öre"
        if six.PY2:
            assert str(err) == "\xc3\xb6re"
        else:
            assert str(err) == u"öre"

    def test_formatting_with_request_id(self):
        err = error.FintectureError(u"öre", headers={"x-request-id": "123"})
        assert six.text_type(err) == u"Request 123: öre"
        if six.PY2:
            assert str(err) == "Request 123: \xc3\xb6re"
        else:
            assert str(err) == u"Request 123: öre"

    def test_formatting_with_none(self):
        err = error.FintectureError(None, headers={"x-request-id": "123"})
        assert six.text_type(err) == u"Request 123: <empty message>"
        if six.PY2:
            assert str(err) == "Request 123: <empty message>"
        else:
            assert str(err) == "Request 123: <empty message>"

    def test_formatting_with_message_none_and_request_id_none(self):
        err = error.FintectureError(None)
        assert six.text_type(err) == u"<empty message>"
        if six.PY2:
            assert str(err) == "<empty message>"
        else:
            assert str(err) == u"<empty message>"

    def test_repr(self):
        err = error.FintectureError(u"öre", headers={"x-request-id": "123"})
        if six.PY2:
            assert (
                repr(err)
                == "FintectureError(message=u'\\xf6re', http_status=None, "
                "x_request_id='123')"
            )
        else:
            assert (
                repr(err) == "FintectureError(message='öre', http_status=None, "
                "x_request_id='123')"
            )

    def test_error_object(self):
        err = error.FintectureError(
            "message", json_body={"error": {"code": "some_error"}}
        )
        assert err.error is not None
        assert err.error.code == "some_error"
        assert err.error.charge is None

    def test_error_object_not_dict(self):
        err = error.FintectureError("message", json_body={"error": "not a dict"})
        assert err.error is None


class TestApiConnectionError(object):
    def test_default_no_retry(self):
        err = error.APIConnectionError("msg")
        assert err.should_retry is False

        err = error.APIConnectionError("msg", should_retry=True)
        assert err.should_retry
