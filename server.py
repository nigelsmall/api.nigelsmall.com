#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bottle import get, post, run, request, response, template, abort
from py2neo.xmlutil import xml_to_cypher, xml_to_geoff


INDEX_TEMPLATE = """\
<!doctype html>
<html>
<head>
</head>
<body>
<h1>Services</h1>
<ul>
<li><a href="/xml-cypher">XML to Cypher Converter</a></li>
<li><a href="/xml-geoff">XML to Geoff Converter</a></li>
</ul>
</body>
</html>
"""

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
<p>See also the <a href="/xml-cypher">XML to Cypher Converter</a>.</p>
</form>
</body>
</html>
"""

XML_CYPHER_TEMPLATE = """\
<!doctype html>
<html>
<head>
<title>XML to Cypher Converter</title>
</head>
<body>
<form method="POST">
<h1>XML to Cypher Converter</h1>
<p>This service allows conversion of generic XML data into a Cypher CREATE statement, which can then be loaded into Neo4j.</p>
<h2>Use as a web service</h2>
To use this API from the command line, use <tt>curl</tt> as below:
<pre>
curl -X POST http://api.nigelsmall.com/xml-cypher -d @test/files/abba.xml
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
<input type="submit" value="Convert to Cypher CREATE statement">
<p>See also the <a href="/xml-geoff">XML to Geoff Converter</a>.</p>
</form>
</body>
</html>
"""


@get("/")
def get_index():
    return template(INDEX_TEMPLATE)


@get("/xml-geoff")
def get_xml_geoff():
    return template(XML_GEOFF_TEMPLATE)


@get("/xml-cypher")
def get_xml_cypher():
    return template(XML_CYPHER_TEMPLATE)


@post("/xml-geoff")
def post_xml_geoff():
    xml = request.POST.get("xml")
    if xml is None:
        xml = request.body.read()
    if xml:
        try:
            response.set_header("Content-Type", "text/plain; charset=UTF-8")
            return xml_to_geoff(xml.strip())
        except:
            abort(400)
    return None


@post("/xml-cypher")
def post_xml_cypher():
    xml = request.POST.get("xml")
    if xml is None:
        xml = request.body.read()
    if xml:
        try:
            response.set_header("Content-Type", "text/plain; charset=UTF-8")
            return xml_to_cypher(xml.strip())
        except:
            abort(400)
    return None


if __name__ == "__main__":
    run(port=9120)

