#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgitb
import cgi
from suunto_hrv import hrv

cgitb.enable()


class Form:
        def __init__(self):
                self.form = """<html><tITLE>Suunto HRV Analysis</title><body>
Upload a Suunto Ambit XML file to determine your HRV. You should record 1-5 minutes of heart rate after a good rest and with controlled breathing. Copy the HRV values to a spreadsheet and adjust your training according to the changes. Read more from e.g. <a href="http://hrvtraining.com">hrvtraining.com</a><br>
<form enctype="multipart/form-data" action="mypy.cgi" method="post">
<p>File: <input type="file" name="file"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body></html>"""

response = """<html><title>Suunto HRV analysis</title><body>
        Results: <br>
                HRV (rmssd) = %f<br>
                HRV (ithlete) = %f<br>
                </body></html>"""

header = """Content-Type: text/html;charset=utf-8

"""

if __name__ == "__main__":
        print header
        form = cgi.FieldStorage()
        try:
                fileitem = form["file"]
                xmldata = fileitem.file.read()
                (hrv_rmssd, hrv_ithlete) = hrv(xmldata)
                print response % (hrv_rmssd, hrv_ithlete)
        except:
                f = Form()
                print f.form


