from __future__ import absolute_import, division, print_function

import datetime
import json
import pickle
from copy import copy, deepcopy

import pytest

import fintecture
from fintecture import six


SAMPLE_CUSTOMER_ACCOUNTS = json.loads(
    """
{
  "data": [
    {
      "attributes": {
        "account_id": "ES5014650100981708392372",
        "account_name": "Rafael Gal\u00e1n Garc\u00eda",
        "account_type": "Compte Courante",
        "bic_swift": "INGDESMMXXX",
        "currency": "EUR",
        "iban": "ES5014650100981708392372",
        "internal_id": "e647314e-863b-4354-a0a0-6037c17f822d"
      },
      "id": "dbfa376561087bbbec64f5f02d0a0dbef1140c124c1b329c8acd731e40a560a3",
      "relationships": {
        "transactions": {
          "links": {
            "related": "https://api-sandbox.fintecture.com/ais/v1/customer/f1923614953cb0e1f1da8b5c016fd5a7/accounts/dbfa376561087bbbec64f5f02d0a0dbef1140c124c1b329c8acd731e40a560a3/transactions"
          }
        }
      },
      "type": "accounts"
    },
    {
      "attributes": {
        "account_id": "ES9214650100921708668748",
        "account_name": "Daniel Bicho Bueno",
        "account_type": "Compte Courante",
        "bic_swift": "INGDESMMXXX",
        "currency": "EUR",
        "iban": "ES9214650100921708668748",
        "internal_id": "7e1f51d4-555d-46d2-9bf9-aab323d4201d"
      },
      "id": "c47c10f6ab228625e9137d82d8b9def0fb7e770eefbfa7c7d36ce818ed7668b3",
      "relationships": {
        "transactions": {
          "links": {
            "related": "https://api-sandbox.fintecture.com/ais/v1/customer/f1923614953cb0e1f1da8b5c016fd5a7/accounts/c47c10f6ab228625e9137d82d8b9def0fb7e770eefbfa7c7d36ce818ed7668b3/transactions"
          }
        }
      },
      "type": "accounts"
    }
  ],
  "meta": {
    "customer_id": "f1923614953cb0e1f1da8b5c016fd5a7",
    "last_authentication": "2022-08-25T19:17:33.216Z",
    "provider": "ingbes",
    "remaining_days": 69
  }
}
"""
)


class TestFintectureObject(object):
    def test_initializes_with_parameters(self):
        obj = fintecture.fintecture_object.FintectureObject(
            "foo", "bar", myparam=5, yourparam="boo"
        )

        assert obj.id == "foo"
        assert obj.app_id == "bar"

    def test_access(self):
        obj = fintecture.fintecture_object.FintectureObject("myid", "mykey", myparam=5)

        # Empty
        with pytest.raises(AttributeError):
            obj.myattr
        with pytest.raises(KeyError):
            obj["myattr"]
        assert obj.get("myattr", "def") == "def"
        assert obj.get("myattr") is None

        # Setters
        obj.myattr = "myval"
        obj["myitem"] = "itval"
        assert obj.setdefault("mydef", "sdef") == "sdef"

        # Getters
        assert obj.setdefault("myattr", "sdef") == "myval"
        assert obj.myattr == "myval"
        assert obj["myattr"] == "myval"
        assert obj.get("myattr") == "myval"

        assert sorted(obj.keys()) == ["app_id", "id", "myattr", "mydef", "myitem"]

        assert sorted(obj.values()) == ["itval", "myid", "mykey", "myval", "sdef"]

        # Illegal operations
        with pytest.raises(ValueError):
            obj.foo = ""

    def test_refresh_from(self, mocker):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"foo": "bar", "trans": "me"}, "myappid"
        )

        assert obj.app_id == "mykey"
        assert obj.foo == "bar"
        assert obj["trans"] == "me"
        assert obj.fintecture_version is None
        assert obj.last_response is None

        last_response = mocker.Mock()
        obj.refresh_from(
            {"foo": "baz", "johnny": 5},
            "key2",
            fintecture_version="2017-08-15",
            last_response=last_response,
        )

        assert obj.johnny == 5
        assert obj.foo == "baz"
        with pytest.raises(AttributeError):
            obj.trans
        assert obj.app_id == "key2"
        assert obj.fintecture_version == "2017-08-15"
        assert obj.last_response == last_response

        obj.refresh_from(
            {"trans": 4, "metadata": {"amount": 42}}, "key2", True
        )

        assert obj.foo == "baz"
        assert obj.trans == 4

    def test_passing_nested_refresh(self):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"foos": {"type": "list", "data": [{"id": "nested"}]}},
            "app_id",
        )

        nested = obj.foos.data[0]

        assert obj.app_id == "app_id"
        assert nested.id == "nested"
        assert nested.app_id == "app_id"

    def test_refresh_from_nested_object(self):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            SAMPLE_CUSTOMER_ACCOUNTS, "app_id"
        )

        assert len(obj.data) == 2

        assert isinstance(obj.data, list)  # TODO: return: fintecture.ListObject
        assert isinstance(obj.meta, fintecture.fintecture_object.FintectureObject)

        # TODO: !! build specialized objects
        assert isinstance(obj.data[0], fintecture.fintecture_object.FintectureObject)

        assert obj.data[0].type == "accounts"

    def test_refresh_from_nested_object_can_be_paged(self):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            SAMPLE_CUSTOMER_ACCOUNTS, "app_id"
        )

        assert len(obj.data) == 2
        assert isinstance(obj.data, list)  # TODO: return: fintecture.ListObject
        # seen = [item["id"] for item in obj.data.auto_paging_iter()]
        # assert seen == [
        #     "dbfa376561087bbbec64f5f02d0a0dbef1140c124c1b329c8acd731e40a560a3",
        #     "c47c10f6ab228625e9137d82d8b9def0fb7e770eefbfa7c7d36ce818ed7668b3"
        # ]

    def test_to_json(self):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            SAMPLE_CUSTOMER_ACCOUNTS, "app_id"
        )

        self.check_invoice_data(json.loads(str(obj)))

    def check_invoice_data(self, data):
        # Check rough structure
        assert len(list(data.keys())) == 20
        assert len(list(data["lines"]["data"][0].keys())) == 22
        assert len(data["lines"]["data"]) == 1

        # Check various data types
        assert data["date"] == 1338238728
        assert data["next_payment_attempt"] is None
        assert data["livemode"] is False
        assert (
            data["lines"]["data"][0]["price"]["billing_scheme"] == "per_unit"
        )

    def test_repr(self):
        obj = fintecture.fintecture_object.FintectureObject("foo", "bar", myparam=5)

        obj["object"] = u"\u4e00boo\u1f00"
        obj.date = datetime.datetime.fromtimestamp(1511136000)

        res = repr(obj)

        if six.PY2:
            res = six.text_type(repr(obj), "utf-8")

        assert u"<FintectureObject \u4e00boo\u1f00" in res
        assert u"id=foo" in res
        assert u'"date": 1511136000' in res

    def test_pickling(self):
        obj = fintecture.fintecture_object.FintectureObject("foo", "bar", myparam=5)

        obj["object"] = "boo"
        obj.refresh_from(
            {
                "fala": "lalala",
                # ensures that empty strings are correctly unpickled in Py3
                "emptystring": "",
            },
            app_id="bar",
        )

        assert obj.fala == "lalala"

        pickled = pickle.dumps(obj)
        newobj = pickle.loads(pickled)

        assert newobj.id == "foo"
        assert newobj.app_id == "bar"
        assert newobj["object"] == "boo"
        assert newobj.fala == "lalala"
        assert newobj.emptystring == ""

    def test_deletion(self):
        obj = fintecture.fintecture_object.FintectureObject("id", "key")

        obj.coupon = "foo"
        assert obj.coupon == "foo"

        del obj.coupon
        with pytest.raises(AttributeError):
            obj.coupon

        obj.refresh_from({"coupon": "foo"}, app_id="bar")
        assert obj.coupon == "foo"

    def test_deletion_metadata(self):
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"metadata": {"key": "value"}}, "myappid"
        )

        assert obj.metadata["key"] == "value"

        del obj.metadata["key"]
        with pytest.raises(KeyError):
            obj.metadata["key"]

    def test_copy(self):
        nested = fintecture.fintecture_object.FintectureObject.construct_from(
            {"value": "bar"}, "myappid"
        )
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"empty": "", "value": "foo", "nested": nested},
            "myappid",
        )

        copied = copy(obj)

        assert copied.empty == ""
        assert copied.value == "foo"
        assert copied.nested.value == "bar"

        assert copied.app_id == "mykey"

        # Verify that we're not deep copying nested values.
        assert id(nested) == id(copied.nested)

    def test_deepcopy(self):
        nested = fintecture.fintecture_object.FintectureObject.construct_from(
            {"value": "bar"}, "myappid"
        )
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"empty": "", "value": "foo", "nested": nested},
            "myappid",
        )

        copied = deepcopy(obj)

        assert copied.empty == ""
        assert copied.value == "foo"
        assert copied.nested.value == "bar"

        assert copied.app_id == "mykey"

        # Verify that we're actually deep copying nested values.
        assert id(nested) != id(copied.nested)

    def test_to_dict_recursive(self):
        foo = fintecture.fintecture_object.FintectureObject.construct_from(
            {"value": "foo"}, "myappid"
        )
        bar = fintecture.fintecture_object.FintectureObject.construct_from(
            {"value": "bar"}, "myappid"
        )
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"empty": "", "value": "foobar", "nested": [foo, bar]}, "myappid"
        )

        d = obj.to_dict_recursive()
        assert d == {
            "empty": "",
            "value": "foobar",
            "nested": [{"value": "foo"}, {"value": "bar"}],
        }
        assert not isinstance(
            d["nested"][0], fintecture.fintecture_object.FintectureObject
        )
        assert not isinstance(
            d["nested"][1], fintecture.fintecture_object.FintectureObject
        )

    def test_serialize_empty_string_unsets(self):
        class SerializeToEmptyString(fintecture.fintecture_object.FintectureObject):
            def serialize(self, previous):
                return ""

        nested = SerializeToEmptyString.construct_from(
            {"value": "bar"}, "mykey"
        )
        obj = fintecture.fintecture_object.FintectureObject.construct_from(
            {"nested": nested}, "myappid"
        )

        assert obj.serialize(None) == {"nested": ""}
