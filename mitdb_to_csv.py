import csv
import wfdb
import numpy as np
import time
import math

print("###################################################")
print("PhysioNet MIT-BIH Arrhythmia Database Record-to-CSV")
print("V 1.1")
print("By Alex Tobias")
print("###################################################")
print()

#initial variable setup
records = ['100','101','102','103','104','105','106','107','108','109','111','112','113','114','115','116','117','118','119','121','122','123','124','200','202','203','205','207','208','209','210','212','213','214','215','217','219','220','221','222','223','228','230','231','232','233','234']

print("Will extract from Records %s." % (", ".join((x for x in records))))
print("Press enter to continue...")

input()

begin_time = time.clock()

for sampleName in records:

	start_time = time.clock()
	print("-------------- RECORD %s --------------" % sampleName)

	#pulling data from mitdb
	print("Getting data for Record " + sampleName + "...")
	signals, fields = wfdb.rdsamp(sampleName, sampfrom=0,sampto='end', pb_dir ='mitdb')
	ann = wfdb.rdann(sampleName, extension='atr',sampfrom=0,shift_samps=False,pb_dir='mitdb',return_label_elements=['symbol',], summarize_labels=False)

	#setting up variables pulled from mitdb file info
	freq = fields.get('fs')
	ecg1 = fields.get('sig_name')[0]
	egc1units = fields.get('units')[0]
	ecg2 = fields.get('sig_name')[1]
	egc2units = fields.get('units')[1]
	numSamples = signals.shape[0]

	#set up our arrays to merge later
	print("Manipulating signal data...")
	samplesArray = np.arange(numSamples)
	signalsArray1 = np.zeros(numSamples)
	signalsArray2 = np.zeros(numSamples)
	timeArray = np.arange(0,(numSamples/freq),(1/freq), dtype = float)
	RArray = np.zeros(numSamples)
	RtypeArray = np.empty(numSamples, dtype = 'str')

	#transform data from annotation to fit in RArray and RtypeArray
	print("Manipulating annotation data...")
	for i in range(numSamples):
		signalsArray1[i] = signals[i,0]
		signalsArray2[i] = signals[i,1]

	for i in ann.sample:
		RArray[i] = 1

	for i in range(ann.sample.shape[0]):
		RtypeArray[ann.sample[i]] = ann.symbol[i]

	#opening & writing to the CSV
	print("Opening CSV file...")
	recordfile = open(sampleName + ".csv","w")
	headers = ["Sample #","Time (s)", ecg1 + " (" + egc1units + ") ", ecg2 + " (" + egc2units + ") ", "R", "Type"]

	print("Writing to CSV file...")

	#creating writer object
	writer = csv.writer(recordfile, dialect = 'excel', lineterminator = '\n')

	#filling headers
	writer.writerow(["Record " + sampleName])
	writer.writerow(headers)

	#values is a list that collects the ith item in each of our arrays
	#for each sample #i, we'll take values and write to the CSV 
	for i in range(numSamples):
		values = [str(samplesArray[i]), str(timeArray[i]), str(signalsArray1[i]), str(signalsArray2[i]), str(RArray[i]), str(RtypeArray[i])]
		writer.writerow(values)

		#progress bar
		if(i%347 == 0 or i+1 == numSamples): 
		#I just threw in a random number so it doesn't need to update each iteration
			percentDone = ((i+1)/numSamples)
			numBar = 16
			bar = "%s%s" % ("#"*math.ceil(numBar*percentDone), "-"*(numBar-math.ceil(numBar*percentDone)))
			print("\r> Progress: [ %s | %.2f%% ], %d rows of %d" % (bar, percentDone*100, i+1, numSamples), end = "")

	print("\nFinished writing to CSV file for Record " + sampleName + ".")
	recordfile.close()

	end_time = time.clock() - start_time
	print("> Time for Record %s: %0.2f seconds." % (sampleName, end_time))

	print()

end_time = time.clock() - begin_time
print("Finished. Total time elapsed = %0.2f seconds." % end_time)
print("Exiting...")
exit()
