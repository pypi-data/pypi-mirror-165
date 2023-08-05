from __future__ import absolute_import, division, print_function

import os

import fintecture
from flask import Flask, request


fintecture.app_id = os.environ.get("FINTECTURE_APP_ID")
fintecture.app_secret = os.environ.get("FINTECTURE_APP_SECRET")
fintecture.access_token = os.environ.get("FINTECTURE_ACCESS_TOKEN")
# fintecture.private_key = os.environ.get("FINTECTURE_PRIVATE_KEY")
fintecture.private_key = """
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDWp2HH1HA0KHnr
jrRs+PmUMU0q+e9hDv9DgxBjHdiwyTIoloPziSNG8jzxvr874qLxZtoYlImbi3IN
sU21RVIa9rLgvr83QwDZDsVw/mhr9VScqi5W9mQJrtSYzgVFZAj9vfml5ERQo7yt
9s4nKJxfcHCWlYzLsdZ6n13ymNl6VopF0nl+c6N3ilf4s5RgwtcphCvrScZ8O14d
kNgEeplcOi0/+Ea+KOLaoajqS1FId2JKv8ByREfLo4YdUWjuUZL/BRJnSR5wxKnC
eXEwqLSa2IGKaOjuqZNVmdqkAPz7Cc8Zx8eBSPOZ2kWbHg6pgFYNOnb2/yyTt53I
050caGx3AgMBAAECggEAZKvm85ICN6weFih9HTid0O9YakYDC2m9tVuURXAbjzol
QJzq8L6KIX19sMFNrhfqZL5gnjOX4DADw0E7GT+UNNor5bUAODo//Qzs88QVlEBg
uQMlrZpsK5Bn2+yP004J23uMSM3obkuEs7AzWnE0+Zvh6fXkrSnQVf1FUgB2yuVL
9nRlpPSE36bJeivQynnbfnFSyR4fxKOaJfmcWE/vyOWFQZG8sPu/AzWXDyJsU5V9
USLC4tGSCOPd41wdGiFOcmUgGsYiEEIkekIs40XUOCmhsIlvA9nygO31odRg1z6y
logOhm/5qBJSYhmj4LGtok+wpvXXb8ROGAtGz9KqtQKBgQD9KFeQA75amaeS7Ses
/IIv+TmhRyWxTydEpIFJkAZEof9PUQE59yJJP9yqXjB1qyY0TvTcT5fvscVaaHg1
TG/gi2k3rSAfvPFRjwn/Gjv2gkbRxvnQXwZxhiNP7eMI53emuu/zT7WxKdR7T767
yaKKA827ElUMfh5cGAU/Qzt0qwKBgQDZEF4UsvKJV9tBiXOROAM4O7UYTZaTiyQ+
G1Nb6oBMeZZN1cl1sKnO581iJ4eoeJnSEtRbUh1hZ5sol/47bAYZBAKDAzxOhvKs
/VJLHgb31wwUlTZBVSgNtbCQd+iePxwW0/dqZXfbVqHcZdl//TeCM5lxjpCk3+io
IwqrMpgvZQKBgD59I8gPtIAGp5+T3JRNrBENctVFi59Ny4KdHLC81V9BoZTBiQz2
3Ma59c0z/MA+4+pLhxOOrhFjjzR2zx1Q5djGcM1mdaR/7g1UwoHuxthdZf/IHsf5
fMyu8K59KOp8wEMup6YmidHWYnWhxJHz/qQUtka0CrxPsUzIPRtVjCqLAoGAcEvQ
cGL3qOhD7U7f9AQHXmM9WDpjqSc188+NO6NBBs9sXA47MGDaKMmxbpNG0ni6E31c
UXZU7tx73+9qPnGvYee6KO9WlsWn7KkNlwEM19FwVYGwVPJqS1Vw5/yw4pWBwamd
eXTPIjFagbxLXrSwr/Jj8uSvniycn8epMFJ3eyUCgYBUW3MSnjkxahF3bCYifEwr
XuM24cO5d7kHoqqpqdF1X4rFOxCXsb4uREooCiqp2CQ+X0PTQVk51v0mnTz3iA4v
Ivc8fsCASr8JfunffWpqiwu9XYwlQWgUVTOO7sN8eSn8EcttVRTwChhm0H2bjjrT
52Z3Kn2G2e6ZotsuvuTtLg==
-----END PRIVATE KEY-----
"""

app = Flask(__name__)


@app.route("/webhooks", methods=["POST"])
def webhooks():
    payload = request.form
    received_digest = request.headers.get("Digest", None)
    received_signature = request.headers.get("Signature", None)
    received_request_id = request.headers.get("X-Request-ID", None)

    try:
        event = fintecture.Webhook.construct_event(
            payload, received_digest, received_signature, received_request_id
        )
    except ValueError:
        print("Error while decoding event!")
        return "Bad payload", 400
    except fintecture.error.SignatureVerificationError as e:
        print("Invalid signature!")
        print("ERROR: %r" % e)
        return "Bad signature", 400

    print(
        "Received event: session_id={session_id}, status={status}, type={type}".format(
            session_id=event.get('session_id'),
            status=event.get('status'),
            type=event.get('type')
        )
    )

    return "", 200


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
