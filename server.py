#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, abort, make_response
from werkzeug.urls import url_decode
from py2neo.xmlutil import xml_to_cypher, xml_to_geoff


application = Flask(__name__)


@application.route("/")
def get_index():
    return render_template("index.html")


@application.route("/xml-geoff")
def get_xml_geoff():
    return render_template("neotool_xml.html", format_title="Geoff", format_description="Geoff interchange file", neotool_command="xml-geoff", see_also={"/xml-cypher": "XML to Cypher converter"})


@application.route("/xml-cypher")
def get_xml_cypher():
    return render_template("neotool_xml.html", format_title="Cypher", format_description="Cypher CREATE statement", neotool_command="xml-cypher", see_also={"/xml-geoff": "XML to Geoff converter"})


def _convert(method):
    body = request.data.decode("utf-8")
    if body.startswith("<"):
        xml = body
    else:
        values = url_decode(body)
        xml = values["xml"]
    if xml:
        try:
            content = method(xml.strip().encode("utf-8"))
            headers = {
                "Content-Type": "text/plain; charset=UTF-8",
            }
            return make_response((content, 200, headers))
        except:
            raise
            abort(400)
    return make_response(("", 204, {}))


@application.route("/xml-geoff", methods=["POST"])
def post_xml_geoff():
    return _convert(xml_to_geoff)


@application.route("/xml-cypher", methods=["POST"])
def post_xml_cypher():
    return _convert(xml_to_cypher)


if __name__ == "__main__":
    application.run(port=9120, debug=True)

