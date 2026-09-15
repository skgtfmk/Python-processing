from com.dotmatics.dataig.studies.dataparser.processor import ExcelFileProcessor
from com.dotmatics.dataig.studies.dataparser.builder import TableBuilder
from com.dotmatics.dataig.studies.dataparser.data import Row
from com.dotmatics.dataig.studies.dataparser.data import CellStatus
from com.dotmatics.dataig.studies.dataparser.util import ScriptUtils

import re, csv
#https://docs.dotmatics.com/platform/6.2/en/studies/how-to-guides/how-to-create-a-python-processing-script.html
def validateCompound(columnID, testValue):
    #Make sure the compound reference exists
    projectId = 0
    if testValue[0:4] == 'ARUK':
        returnType = 'validate'
        if len(testValue) == 11:
            projectId = 45000 #SCREENING_COLLECTION
            dataSourceKeys = '914_FORMATTED_ID'
        elif len(testValue) == 15:
            projectId = 55000 #DICTIONARIES
            dataSourceKeys = '1154_FORMATTED_BATCH_ID'
        elif len(testValue) == 19:
            projectId = 55000 #DICTIONARIES
            dataSourceKeys = '1155_FORMATTED_SAMPLE_ID'
        else:
            projectId = 45000 #SCREENING_COLLECTION
            dataSourceKeys = '914_FORMATTED_ID'
    else:
        returnType = 'convert'
        projectId = 56000 #DICT_SUPPLIER_REF
        dataSourceKeys = '1167_SUPPLIER_REF,1167_FORMATTED_ID'  #1167 is a lookup based on SUPPLIER_REF

    logger.info ('Project ID is ' + str(projectId) + ', Datasource key is ' + dataSourceKeys + ' Test value is ' + testValue)
    cmpdMap = util.getProjectData(projectId, dataSourceKeys, testValue)
    supplier_map = cmpdMap[testValue]    
 #   logger.info('Converting ' + testValue + ' supplier map ' + supplier_map.getDataSources()['56000']['1']['FORMATTED_ID'])

    if supplier_map.isEmpty() is True:
        returnValue = testValue
        msg = 'Invalid sample ID'
    else:
        returnValue = testValue
        msg = ''
        if returnType == 'convert':
            logger.info('Got to the Convert part')
            returnValue = supplier_map.getDataSources()[56000][1]['FORMATTED_ID']
    logger.info('ARUK number for ' + testValue + ' is ' + str(returnValue))

    sampleIDcell = row.addCell(columnID, returnValue)
    if msg != '':
        sampleIDcell.setStatus(CellStatus.ERROR)
        sampleIDcell.setMessage(msg)

def validateMissing(columnID, testValue, seriousness):
    #Check if a value is missing and report.
    #seriousness = ['ERROR','WARN']
    sampleIDcell = row.addCell(columnID, testValue)
    if testValue is None:
        if seriousness == 'ERROR':
            sampleIDcell.setStatus(CellStatus.ERROR)
            sampleIDcell.setMessage('Value required')
        else:
            sampleIDcell.setStatus(CellStatus.WARN)
            sampleIDcell.setMessage('Value recommended')

def validateOrganismStrain(columnID, testValue, insertValue, seriousness):
    #Check if the organism (strain) is valid. testValue must be in that format, e.g. "Mouse (CD-1)".
    #seriousness = ['ERROR','WARN']
#    logger.info(testValue + ' insert ' + insertValue)
    sampleIDcell = row.addCell(columnID, insertValue)
    projectId = 55000 #DICTIONARIES
    dataSourceKeys = '1146_ADME_ORGANISM'
    speciesMap = util.getProjectData(projectId, dataSourceKeys, testValue)
    if speciesMap[testValue].isEmpty() is True:
        if seriousness == 'ERROR':
            sampleIDcell.setStatus(CellStatus.ERROR)
        else:
            sampleIDcell.setStatus(CellStatus.WARN)
        sampleIDcell.setMessage(testValue + ' is an invalid ORGANISM (STRAIN)')

#parse excel file
fp = ExcelFileProcessor(data.getFile())
f = fp.process()
  
#get sheet 1
sheet1 = f.getSheetByName('Dotmatics Upload')

#define table
table1 = TableBuilder.build('CRO_PKA_TITRATION_DATA')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatchId = table1.getColumnByName('BATCH_ID')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')
tcCro = table1.getColumnByName('CRO')
tcCroDate = table1.getColumnByName('CRO_DATE')
tcPka1Qual = table1.getColumnByName('PKA_1_QUAL')
tcPka1 = table1.getColumnByName('PKA_1')
tcPka1Sd = table1.getColumnByName('PKA_1_SD')
tcPka2Qual = table1.getColumnByName('PKA_2_QUAL')
tcPka2 = table1.getColumnByName('PKA_2')
tcPka2Sd = table1.getColumnByName('PKA_2_SD')
tcPkaStructureNote = table1.getColumnByName('PKA_STRUCTURE_NOTE')
tcComments = table1.getColumnByName('COMMENTS')
tcOrderBy = table1.getColumnByName('ORDER_BY')

logger.info('running script CRO_PKA_TITRATION_DATA ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    validateCompound(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatchId, sheet1.getCellValue(r,1))
    row.addCell(tcStudyName, sheet1.getCellValue(r,2))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,3))
    row.addCell(tcCro, sheet1.getCellValue(r,4))
    row.addCell(tcCroDate, sheet1.getCellValue(r,5))

    row.addCell(tcPka1Qual, sheet1.getCellValue(r,6))
    row.addCell(tcPka1, sheet1.getCellValue(r,7))
    row.addCell(tcPka1Sd, sheet1.getCellValue(r,8))
    row.addCell(tcPka2Qual, sheet1.getCellValue(r,9))
    row.addCell(tcPka2, sheet1.getCellValue(r,10))
    row.addCell(tcPka2Sd, sheet1.getCellValue(r,11))
    row.addCell(tcPkaStructureNote, sheet1.getCellValue(r,12))
    row.addCell(tcComments, sheet1.getCellValue(r,13))
    row.addCell(tcOrderBy, r)

logger.info('CRO_PKA_TITRATION_DATA script finished')