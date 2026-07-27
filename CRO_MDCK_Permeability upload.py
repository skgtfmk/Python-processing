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
table1 = TableBuilder.build('CRO_MDCK_PERM')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatch = table1.getColumnByName('BATCH')
tcCro = table1.getColumnByName('CRO')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcPappa2B = table1.getColumnByName('PAPPA2B')
tcPappb2A = table1.getColumnByName('PAPPB2A')
tcPappUnits = table1.getColumnByName('PAPP_UNITS')
tcEffluxRatio = table1.getColumnByName('EFFLUX_RATIO')
tcRecovA2B = table1.getColumnByName('RECOV_A2B')
tcRecovB2A = table1.getColumnByName('RECOV_B2A')
tcTransfection = table1.getColumnByName('TRANSFECTION')
tcInhibitorPresent = table1.getColumnByName('INHIBITOR_PRESENT')
tcPappa2BQualifier = table1.getColumnByName('PAPPA2B_QUALIFIER')
tcPappb2AQualifier = table1.getColumnByName('PAPPB2A_QUALIFIER')
tcEffluxRatioQualifier = table1.getColumnByName('EFFLUX_RATIO_QUALIFIER')
tcRecovA2BQualifier = table1.getColumnByName('RECOV_A2B_QUALIFIER')
tcRecovB2AQualifier = table1.getColumnByName('RECOV_B2A_QUALIFIER')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')


logger.info('running script CRO_MDCK_PERM ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    row.addCell(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatch, sheet1.getCellValue(r,1))
    row.addCell(tcCro, sheet1.getCellValue(r,2))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,3))
    row.addCell(tcPappa2B, sheet1.getCellValue(r,4))
    row.addCell(tcPappb2A, sheet1.getCellValue(r,5))
    row.addCell(tcPappUnits, sheet1.getCellValue(r,6))
    row.addCell(tcEffluxRatio, sheet1.getCellValue(r,7))
    row.addCell(tcRecovA2B, sheet1.getCellValue(r,8))
    row.addCell(tcRecovB2A, sheet1.getCellValue(r,9))
    row.addCell(tcTransfection, sheet1.getCellValue(r,10))
    row.addCell(tcInhibitorPresent, sheet1.getCellValue(r,11))
    row.addCell(tcPappa2BQualifier, sheet1.getCellValue(r,12))
    row.addCell(tcPappb2AQualifier, sheet1.getCellValue(r,13))
    row.addCell(tcEffluxRatioQualifier, sheet1.getCellValue(r,14))
    row.addCell(tcRecovA2BQualifier, sheet1.getCellValue(r,15))
    row.addCell(tcRecovB2AQualifier, sheet1.getCellValue(r,16))
    row.addCell(tcStudyName, sheet1.getCellValue(r,17))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,18))

logger.info('CRO_MDCK_PERM script finished')