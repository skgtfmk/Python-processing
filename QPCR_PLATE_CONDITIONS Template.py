from com.dotmatics.dataig.studies.dataparser.processor import ExcelFileProcessor
from com.dotmatics.dataig.studies.dataparser.builder import TableBuilder
from com.dotmatics.dataig.studies.dataparser.data import Row
import re, csv

#parse excel file
fp = ExcelFileProcessor(data.getFile())
f = fp.process()
  
#get sheet 1
sheet1 = f.getSheetByName('Plate Conditions')

#define table
table1 = TableBuilder.build('QPCR_PLATE_CONDITIONS')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcPlateBarcode = table1.getColumnByName('PLATE_BARCODE')
tcConditionType = table1.getColumnByName('CONDITION_TYPE')
tcConditionValue = table1.getColumnByName('CONDITION_VALUE')
tcExperimentValue = table1.getColumnByName('EXPERIMENT_VALUE')

logger.info('running script QPCR_PLATE_CONDITIONS...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    row.addCell(tcPlateBarcode, sheet1.getCellValue(r,0))
    row.addCell(tcConditionType, sheet1.getCellValue(r,1))
    row.addCell(tcConditionValue, sheet1.getCellValue(r,2))
    row.addCell(tcExperimentValue, sheet1.getCellValue(r,3))
    
logger.info('QPCR_PLATE_CONDITIONS script finished')