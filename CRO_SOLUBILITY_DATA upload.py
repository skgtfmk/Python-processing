from com.dotmatics.dataig.studies.dataparser.processor import ExcelFileProcessor
from com.dotmatics.dataig.studies.dataparser.builder import TableBuilder
from com.dotmatics.dataig.studies.dataparser.data import Row
import re, csv

#parse excel file
fp = ExcelFileProcessor(data.getFile())
f = fp.process()
  
#get sheet 1
sheet1 = f.getSheetByName('Dotmatics Upload')

#define table
table1 = TableBuilder.build('CRO_SOLUBILITY_DATA')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatch = table1.getColumnByName('BATCH')
tcCro = table1.getColumnByName('CRO')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcPh = table1.getColumnByName('PH')
tcSolUm = table1.getColumnByName('SOL_UM')
tcQualifier = table1.getColumnByName('QUALIFIER')
tcComments = table1.getColumnByName('COMMENTS')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')

logger.info('running script CRO_SOLUBILITY_DATA ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    row.addCell(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatch, sheet1.getCellValue(r,1))
    row.addCell(tcCro, sheet1.getCellValue(r,2))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,3))
    row.addCell(tcPh, sheet1.getCellValue(r,4))
    row.addCell(tcSolUm, sheet1.getCellValue(r,5))
    row.addCell(tcQualifier, sheet1.getCellValue(r,6))
    row.addCell(tcComments, sheet1.getCellValue(r,7))
    row.addCell(tcStudyName, sheet1.getCellValue(r,8))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,9))

logger.info('CRO_SOLUBILITY_DATA script finished')