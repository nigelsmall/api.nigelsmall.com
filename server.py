#!/usr/bin/env python
# -*- coding: utf-8 -*-


from StringIO import StringIO
from bottle import get, post, run, request, response, template, abort, redirect
from py2neo import geoff


XML_GEOFF_TEMPLATE = """\
<!doctype html>
<html>
<head>
<title>XML to Geoff Converter</title>
</head>
<body>
<form method="POST">
<h1>XML to Geoff Converter</h1>
<textarea name="xml" cols="80" rows="24"></textarea>
<br>
<input type="submit" value="Convert to Geoff">
</form>
</body>
</html>
"""


@get("/")
def get_index():
    return redirect("/neotool/xml-geoff/")


@get("/neotool/xml-geoff")
def get_neotool_xml_geoff_no_slash():
    return redirect("/neotool/xml-geoff/")


@get("/neotool/xml-geoff/")
def get_neotool_xml_geoff():
    return template(XML_GEOFF_TEMPLATE)


@post("/neotool/xml-geoff/")
def post_neotool_xml_geoff():
    xml = request.POST.get("xml")
    if xml is None:
        xml = request.body.read()
    if xml:
        try:
            subgraph = geoff.Subgraph.load_xml(StringIO(xml.decode("utf-8")))
            response.set_header("Content-Type", "text/plain; charset=UTF-8")
            return subgraph._source
        except:
            abort(400)
    return None


if __name__ == "__main__":
    run(host="0.0.0.0", port=9120)

