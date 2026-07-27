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
table1 = TableBuilder.build('CRO_MICROSOMAL_STAB')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatch = table1.getColumnByName('BATCH')
tcCro = table1.getColumnByName('CRO')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcSpecies = table1.getColumnByName('SPECIES')
tcClintMic = table1.getColumnByName('CLINT_MIC')
tcClintMic_Units = table1.getColumnByName('CLINT_MIC_UNITS')
tcClintLiver = table1.getColumnByName('CLINT_LIVER')
tcClintLiver_Units = table1.getColumnByName('CLINT_LIVER_UNITS')
tcHalfLife_Qualifier = table1.getColumnByName('HALF_LIFE_QUALIFIER')
tcHalfLife_Min = table1.getColumnByName('HALF_LIFE_MIN')
tcR2 = table1.getColumnByName('R2')
tcWcfRemaining_60Min = table1.getColumnByName('WCF_REMAINING_60MIN')
tcNcfRemaining_60Min = table1.getColumnByName('NCF_REMAINING_60MIN')
tcKElimination_Per_Min = table1.getColumnByName('K_ELIMINATION_PER_MIN')
tcUploadDate = table1.getColumnByName('UPLOAD_DATE')
tcTimeMin = table1.getColumnByName('TIME_MIN')
tcPctRemaininig_Ts = table1.getColumnByName('PCT_REMAININIG_TS')
tcLnPct_Remaininig_Ts = table1.getColumnByName('LN_PCT_REMAININIG_TS')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')

logger.info('running script CRO_MICROSOMAL_STAB ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    row.addCell(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatch, sheet1.getCellValue(r,1))
    row.addCell(tcCro, sheet1.getCellValue(r,2))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,3))
    row.addCell(tcSpecies, sheet1.getCellValue(r,4))
    row.addCell(tcClintMic, sheet1.getCellValue(r,5))
    row.addCell(tcClintMic_Units, sheet1.getCellValue(r,6))
    row.addCell(tcClintLiver, sheet1.getCellValue(r,7))
    row.addCell(tcClintLiver_Units, sheet1.getCellValue(r,8))
    row.addCell(tcHalfLife_Qualifier, sheet1.getCellValue(r,9))
    row.addCell(tcHalfLife_Min, sheet1.getCellValue(r,10))
    row.addCell(tcR2, sheet1.getCellValue(r,11))
    row.addCell(tcWcfRemaining_60Min, sheet1.getCellValue(r,12))
    row.addCell(tcNcfRemaining_60Min, sheet1.getCellValue(r,13))
    row.addCell(tcKElimination_Per_Min, sheet1.getCellValue(r,14))
#    row.addCell(tcUploadDate, sheet1.getCellValue(r,15))
    row.addCell(tcTimeMin, sheet1.getCellValue(r,16))
    row.addCell(tcPctRemaininig_Ts, sheet1.getCellValue(r,17))
    row.addCell(tcLnPct_Remaininig_Ts, sheet1.getCellValue(r,18))
    row.addCell(tcStudyName, sheet1.getCellValue(r,19))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,20))

logger.info('CRO_MICROSOMAL_STAB script finished')