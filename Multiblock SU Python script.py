# Read blocks of data from an Excel file.
# Each block starts at the line following a regular expression from the per-study
# property "Block identifier" and runs for for the full size of the plate.
# The actual value is stored in the plate property "block identifier".
# The property "Raw data layer" determines which layer is used to calculate Plate Median and MAD.

from com.dotmatics.dataig.studies import StudyUtils
from java.io import File
import re, os
import datetime

def Calc_median(list_data):
    list_data.sort()
    mid = len(list_data)//2
    return (list_data[mid] + list_data[~mid])/2

# 1-indexed column in which the data block starts.
data_start_column = 2
numrows = results.getNumRows()
numcols = results.getNumCols()
# Read data from file.
f = StudyUtils.convertExcelToArrayList(File(orig_file))
plate_name = os.path.splitext(os.path.basename(orig_file))[0]

max_row = len(f)
properties = results.getExperimentProperties()
if 'Block identifier' in properties:
    start_regex = properties.get('Block identifier').getPropertyValue()
else:
    start_regex = '\d\. .*\((.*)\)' #'\d{1,2}(\t\d{1,2})+' #'\d\. .*'
if 'Raw data layer' in properties:
    raw_data_layer = properties.get('Raw data layer').getPropertyValue()
else:
    raw_data_layer = 1
    
#logger.info(f[13])
plate_n = 0
current_row = 0
regex_match = []
blockFound = False
plate_id = ''
plate_date = ''

# Loop for each plate.
    # Look for start regex.
while current_row < max_row:
#    logger.info(str(current_row)+ '.'.join(f[current_row]))
#    logger.info(f[current_row])
    #Get plate ID and the date/time
    re_prop = re.search('ID(\d):\s*(.+?)\s*$',','.join(f[current_row]))
    if re_prop:
 #       logger.info(re_prop.group(1), re_prop.group(2))
        try:
            if re_prop.group(1) == '1':
                plate_id = re_prop.group(2)
            elif re_prop.group(1) == '3':
                plate_date = re_prop.group(2)
        except:
            plate_id = 'Plate ' + str(plate_n)
            plate_date = datetime.datetime.now()
#        logger.info('Plate name = ' + plate_id + 'Date =' + str(plate_date))

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
        # Wait until the correct layer before calculating the plate stats
        plateMedian = Calc_median(myTSarray)
        ts_result_AD = [abs(x - plateMedian) for x in myTSarray]
        plateMAD = Calc_median(ts_result_AD)*1.4826
        logger.info('Raw data layer=' + str(raw_data_layer) +' Plate number=' + str(plate_n) + ' Median=' + str(plateMedian) + ' MAD=' + str(plateMAD))
#        myplate = results.get(0)
        if plate_n+1 == int(raw_data_layer):
            myplate.addProperty('Plate_Median', str(plateMedian))
            myplate.addProperty('Plate_MAD', str(plateMAD))
        myplate.addProperty('HTRF block', block_label)
        myplate.setName(block_label + '_' + plate_name)
        plate_n += 1
