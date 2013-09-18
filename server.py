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
<p>This service allows conversion of generic XML data into Geoff, which can then be loaded into Neo4j.</p>
<h2>Use as a web service</h2>
To use this API from the command line, use <tt>curl</tt> as below:
<pre>
curl -X POST http://api.nigelsmall.com/xml-geoff -d @test/files/abba.xml
</pre>
<h2>Try on this page</h2>
<textarea name="xml" cols="80" rows="24" wrap="off"><?xml version="1.0" encoding="UTF-8" ?>
<group id="abba">
  <member id="agnetha">
    <name>Agnetha Fältskog</name>
    <birth date="1950-04-05" />
  </member>
  <member id="björn">
    <name>Björn Ulvaeus</name>
    <birth date="1945-04-25" />
  </member>
  <member id="benny">
    <name>Benny Andersson</name>
    <birth date="1946-12-16" />
  </member>
  <member id="frida">
    <name>Anni-Frid Lyngstad</name>
    <birth date="1945-11-15" />
  </member>
  <song id="waterloo" release_date="1974-03-04">
    <name>Waterloo</name>
    <length min="2" sec="42" />
  </song>
</group>
</textarea>
<br>
<input type="submit" value="Convert to Geoff">
</form>
</body>
</html>
"""


@get("/")
def get_index():
    return redirect("/xml-geoff")


@get("/xml-geoff")
def get_xml_geoff():
    return template(XML_GEOFF_TEMPLATE)


@post("/xml-geoff")
def post_xml_geoff():
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
    run(port=9120)

