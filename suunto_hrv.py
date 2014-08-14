#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgitb
import cgi
from suunto_hrv import hrv, read_ibi, filter_rr
import numpy
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import pylab

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
	<table>
<tr><td>Filename</td><td>HRV (RMSSD)</td><td>HRV (ithlete)</td><td>RR data</td></tr>
<tr><td>%s</td><td>%f</td><td>%f</td><td><img src="%s"></td></tr>
</table>	
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
		rr = filter_rr(read_ibi(xmldata))
		t = numpy.linspace(0, rr.sum(), len(rr))
		pylab.plot(t, rr)
		img_name = "rr.png"
		pylab.savefig(img_name)
		print response % (fileitem.filename, hrv_rmssd, hrv_ithlete, img_name)
	except:
		f = Form()
		print f.form

