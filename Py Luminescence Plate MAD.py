# Read blocks of data from an Excel or csv file.
# Each block starts at the line following a regular expression from the per-study
# property "block identifier" and runs for for the full size of the plate.
# The actual value is stored in the plate property "block identifier".
from com.dotmatics.dataig.studies import StudyUtils
from java.io import File
import re, os
import csv
from datetime import datetime

def Calc_median(list_data):
    list_data.sort()
    mid = len(list_data)//2
    return (list_data[mid] + list_data[~mid])/2

def txt_reader(file_path, dialect):
    fle = open(file_path, "r")
    reader = csv.reader(fle, dialect)
    return([line for line in reader])

def read_data(data_path):
    file_ext = os.path.splitext(data_path)[1].lower()
    if file_ext in [".xlsx", ".xls"]:
        file_data = StudyUtils.convertExcelToArrayList(File(data_path))
    elif file_ext == ".csv":
        file_data = txt_reader(data_path, "excel")
    elif file_ext == ".txt":
        file_data = txt_reader(data_path, "excel-tab")
    else:
        exit("File format: %s is unsupported" % file_ext)
    return file_data

def get_plate_parameters (fContents):
    current_r =0
    lPlate_Id = None
    lPlate_date = None
    while current_r < len(fContents) :
        if lPlate_Id is None:
            re_prop = re.search('ID1: ([^,\n]*)',','.join(fContents[current_r]))
            if re_prop:
        #       logger.info(re_prop.group(1), re_prop.group(2))
                lPlate_Id = re_prop.group(1)
        if lPlate_date is None:
            re_prop = re.search('ID3: ([^\n]*)',','.join(fContents[current_r]))
            if re_prop:
        #       logger.info(re_prop.group(1), re_prop.group(2))
                dt = datetime.strptime(re_prop.group(1), "%d/%m/%Y,%H:%M:%S")
                lPlate_date = dt.strftime("%d %b %Y %H:%M:%S")
        current_r += 1
        if lPlate_Id is not None and lPlate_date is not None:
            break
    logger.info(lPlate_date )
    return lPlate_Id, lPlate_date

# 1-indexed column in which the data block starts.
data_start_column = 2
numrows = results.getNumRows()
numcols = results.getNumCols()
# Read data from file.
f = read_data(orig_file)
#f = StudyUtils.convertExcelToArrayList(File(orig_file))

#set the default plate name to the file name
plate_name = os.path.splitext(os.path.basename(orig_file))[0]
#Look for a plate number in the file name
re_name = re.search('plate \d{1,2}', plate_name, re.I)
if re_name:
    plate_name = re_name.group(0)
plate_id, plate_date = get_plate_parameters(f)

max_row = len(f)
properties = results.getExperimentProperties()
if 'block identifier' in properties:
    start_regex = properties.get('block identifier').getPropertyValue()
else:
    start_regex = 'Raw Data[^,]*'

plate_id, plate_date = get_plate_parameters(f)

plate_n = 0
current_row = 0
regex_match = []
# Loop for each plate.
    # Look for start regex.
while current_row < max_row:
    regex_match = re.findall(start_regex, ','.join(f[current_row]))
    current_row += 1
    if len(regex_match) > 0:
        break
#if len(regex_match) == 0 or current_row >= max_row:
#    break
# Plate 0 is the 1st plate and is pre-prepared before the Python process starts.
# Other plates need to be added before use.
if plate_n > 0:
    results.add()

myplate = results.get(plate_n)
myplate.addProperty('Raw Data Block', regex_match[0])
myarray = myplate.getResults()
myTSarray = []
# Add data to array.
row_n = 0
current_row += 1  #Ignore the column labels
while current_row < max_row and row_n < numrows:
    this_row = f[current_row]
    current_row += 1
    for column_n in range(min(len(this_row) - data_start_column + 1, numcols)):
        try:
            myarray[row_n][column_n] = float(this_row[column_n + data_start_column - 1])
            myTSarray.append(myarray[row_n][column_n])
        except ValueError:
            pass
    row_n += 1
plateMedian = Calc_median(myTSarray)
myplate.addProperty('Plate_Median', str(plateMedian))
ts_result_AD = [abs(x - plateMedian) for x in myTSarray]
plateMAD = Calc_median(ts_result_AD)*1.4826
myplate.addProperty('Plate_MAD', str(plateMAD))
myplate.addProperty('Read Time', plate_date)
myplate.setName(plate_name)
myplate.setBarcode(plate_id)
plate_n += 1