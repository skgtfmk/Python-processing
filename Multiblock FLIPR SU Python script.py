# Read blocks of data from an Excel file.
# Each block starts at the line following a regular expression from the per-study
# property "Block identifier" and runs for for the full size of the plate.
# The actual value is stored in the plate property "block identifier".
# The property "Raw data layer" determines which layer is used to calculate Plate Median and MAD.

from com.dotmatics.dataig.studies import StudyUtils
from java.io import File
import re
import datetime
import os.path
import csv

def Calc_median(list_data):
    list_data.sort()
    mid = len(list_data)//2
    return (list_data[mid] + list_data[~mid])/2
def get_HTRF_block(layerName):
    htrfBlock = {"337/665 A":"665nm", "337/620 B":"620nm",
        "337 / 665 / 620":"Ratio","calculated":"Interpolated data"}
    if layerName in htrfBlock.keys():
        return htrfBlock[layerName]
    else:
        return layerName

def txt_reader(file_path, dialect):
    fle = open(file_path, "r")
    reader = csv.reader(fle, dialect)
    return([line for line in reader])
def read_data(data_path):
    file_ext = os.path.splitext(data_path)[1]
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
    lplate_time = None
    while current_r < len(fContents) :
        if lPlate_Id is None:
            re_prop = re.search('File = (.*).fmp',','.join(fContents[current_r]))
            if re_prop:
        #       logger.info(re_prop.group(1), re_prop.group(2))
                try:
                    lPlate_Id = os.path.basename(re_prop.group(1))
                except:
                    lPlate_Id = 'Plate ' + str(plate_n)
        if lPlate_date is None:
            re_prop = re.search('End Date = (.*)',','.join(fContents[current_r]))
            if re_prop:
        #       logger.info(re_prop.group(1), re_prop.group(2))
                try:
                    lPlate_date = re_prop.group(1)
                except:
                    lPlate_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if lplate_time is None:
            re_prop = re.search('End Time = (.*)',','.join(fContents[current_r]))
            if re_prop:
        #       logger.info(re_prop.group(1), re_prop.group(2))
                try:
                    lplate_time = re_prop.group(1)
                except:
                    lplate_time = datetime.datetime.today().strftime('%H:%M:%S')
        current_r += 1
    logger.info(lPlate_date, lplate_time )
    return lPlate_Id, lPlate_date + ' ' + lplate_time

# 1-indexed column in which the data block starts.
data_start_column = 2
numrows = results.getNumRows()
numcols = results.getNumCols()
# Read data from file.
f = read_data(orig_file)
#f = StudyUtils.convertExcelToArrayList(File(orig_file))
#Default plate name is the file name. Otherwise, look for the word 'plate' in the file name
plate_name = os.path.splitext(os.path.basename(orig_file))[0]
re_name = re.search('plate \d{1,2}', plate_name, re.I)
if re_name:
    plate_name = re_name.group(0)
    
max_row = len(f)
properties = results.getExperimentProperties()
if 'Block identifier' in properties:
    start_regex = properties.get('Block identifier').getPropertyValue()
else:
    start_regex = 'Statistic = (.*)' 

#Get raw data layer on which to calculate plate statistics
if 'Raw data layer' in properties:
    raw_data_layer = properties.get('Raw data layer').getPropertyValue()
else:
    raw_data_layer = 0
    
logger.info('Raw data layer ' + raw_data_layer)
plate_n = 0
current_row = 0
regex_match = []
blockFound = False
plate_id = ''
plate_date = ''

plate_id, plate_date = get_plate_parameters(f)
# Loop for each plate.
    # Look for start regex.
while current_row < max_row:
#    logger.info(str(current_row)+ '.'.join(f[current_row]))
#    logger.info(f[current_row])
    #Get plate ID and the date/time

    regex_match = re.search(start_regex, ','.join(f[current_row]))
    current_row += 1
    if regex_match:
        blockFound = True
    if blockFound:
        blockFound = False
        logger.info('Block found on ' + str(current_row) + ': ' + regex_match.group(0))
        
        try:
            block_label = regex_match.group(1)
        except:
            block_label = regex_match.group(0)

        # Plate 0 is the 1st plate and is pre-prepared before the Python process starts.
        # Other plates need to be added before use.
        if plate_n > 0:
            results.add()

        myplate = results.get(plate_n)
        if plate_n ==0:
            myplate.setName(plate_id)
            myplate.setBarcode(plate_id)
            myplate.setTime(plate_date)

    #   myplate.addProperty('block identifier', regex_match[0])
        myarray = myplate.getResults()
        myTSarray = []
        # Add data to array.
        row_n = 0
        current_row += 2  #Ignore the column labels
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
        # Wait until the correct layer before calculating the plate stats
        plateMedian = Calc_median(myTSarray)
        ts_result_AD = [abs(x - plateMedian) for x in myTSarray]
        plateMAD = Calc_median(ts_result_AD)*1.4826
        logger.info('Raw data layer=' + str(raw_data_layer) +' Plate number=' + str(plate_n) + ' Median=' + str(plateMedian) + ' MAD=' + str(plateMAD))
#        myplate = results.get(0)
        if raw_data_layer > 0:
            if plate_n+1 == int(raw_data_layer):
                myplate.addProperty('Plate_Median', str(plateMedian))
                myplate.addProperty('Plate_MAD', str(plateMAD))
        else:
            myplate.addProperty('Plate_Median', str(plateMedian))
            myplate.addProperty('Plate_MAD', str(plateMAD))

        myplate.addProperty('Raw Data Block', block_label)
        myplate.addProperty('Plate End Time', plate_date)
        myplate.addProperty('Source File', plate_id)
        myplate.setName(block_label + "-" + plate_name)
        myplate.setBarcode(plate_name)
        plate_n += 1
