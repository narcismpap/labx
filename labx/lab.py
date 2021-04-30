# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

import base64

from flask import Flask, request, jsonify, Response

from model_result import Result
from decode_qr import parse_qr, QRParseError
from signature import add_signature


def create_app():
    app = Flask(__name__)
    app.debug = True  # @todo: properly

    # Generate a QR Code payload server-side for a given test ID
    @app.route("/api/1.0/qr/<test_id>/")
    def qr_generate(test_id):
        r = Result()
        r.load_from_db(test_id)  # mocked for now
        return add_signature(r.to_qr())

    # Verify the QR Code payload server-side
    # client-side app should perform validation directly work can be also off-loaded to this API (offline checks)
    # QR code payload must be POSTed
    @app.route("/api/1.0/verify/", methods=["POST"])
    def verify():
        try:
            r = parse_qr(request.form.get("qr"))
            return jsonify(r.to_dict())
        except QRParseError as e:
            return Response(str(e), status=400)

    # Return the test results for a given test ID (online checks)
    @app.route("/api/1.0/result/<test_id>/")
    def result(test_id):
        r = Result()
        r.load_from_db(test_id)
        return jsonify(r.to_dict())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001)
