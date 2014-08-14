#!/usr/bin/python
# read Suunto XML and determine some HRV values

import sys
import numpy
import math

def read_ibi_from_xml(filename):
	return read_ibi(open(filename).read())

def read_ibi(xmldata):
	# parse IBI values from the Suunto Ambit created XML
	
	ibi_s = xmldata.find("<IBI>")
	ibi_e = xmldata.find("</IBI>")

	rr_raw = xmldata[ibi_s+5:ibi_e].split(" ")
	rr_raw = numpy.array([int(r) for r in rr_raw])
	return rr_raw


def filter_rr (rr):
	# to be improved 

	min_hr = 30
	max_hr = 200

	max_rri = 1.0 / (min_hr / 60.0) * 1000
	min_rri = 1.0 / (max_hr / 60.0) * 1000

	rr_filtered = []
	for r in rr:
		if r >= min_rri and r <= max_rri:
			rr_filtered.append(r)

	return numpy.array(rr_filtered)


def hrv_rmssd(rr):
	# Calculate Heart rate variability (RMSSD)
	sd = numpy.diff(rr)

	sq = [d**2 for d in sd]

	return (numpy.mean(sq))**(0.5)

def hrv_ithlete(rmssd):
	# Scale the heart rate variability like the application ithlete does
	# according to http://hrvtraining.com/2013/07/04/rmssd-the-hrv-value-provided-by-ithlete-and-bioforce/
	return 20 * math.log(rmssd)

def hrv(xmldata):
	rr_raw = read_ibi(xmldata)
	rr = filter_rr(rr_raw)
	hrvrmssd = hrv_rmssd(rr)
	hrvithlete = hrv_ithlete(hrvrmssd)
	return (hrvrmssd, hrvithlete)

if __name__ == "__main__":
	rr_raw = read_ibi_from_xml(sys.argv[1])
	rr = filter_rr(rr_raw)

	print "HRV (RMSSD) = %f" % hrv_rmssd(rr) 
	print "HRV (ithlete) = %f" % hrv_ithlete(hrv_rmssd(rr))
