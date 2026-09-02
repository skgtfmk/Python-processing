from com.dotmatics.dataig.studies.dataparser.processor import ExcelFileProcessor
from com.dotmatics.dataig.studies.dataparser.builder import TableBuilder
from com.dotmatics.dataig.studies.dataparser.data import Row
from com.dotmatics.dataig.studies.dataparser.data import CellStatus
from com.dotmatics.dataig.studies.dataparser.util import ScriptUtils

import re, csv

def validateCompound(columnID, testValue):
    #Make sure the compound reference exists
    projectId = 0
    if testValue[0:4] == 'ARUK':
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
        projectId = 45000 #SCREENING_COLLECTION
        dataSourceKeys = '914_FORMATTED_ID' #'1153_FORMATTED_ID' #1153 is a lookup based on SUPPLIER_REF

    cmpdMap = util.getProjectData(projectId, dataSourceKeys, testValue)
#    logger.info(dataSourceKeys)
#    logger.info(cmpdMap[testValue])
    sampleIDcell = row.addCell(columnID, testValue)
    if cmpdMap[testValue].isEmpty() is True:
        sampleIDcell.setStatus(CellStatus.ERROR)
        sampleIDcell.setMessage('Invalid sample ID')

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
table1 = TableBuilder.build('CRO_HEPATOCYTE_STAB')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatch = table1.getColumnByName('BATCH')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')
tcCro = table1.getColumnByName('CRO')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcSpecies = table1.getColumnByName('SPECIES')
tcOrganismStrain = table1.getColumnByName('ORGANISM_STRAIN')
tcSex = table1.getColumnByName('SEX')
tcClintHep = table1.getColumnByName('CLINT_HEP')
tcClintHepUnits = table1.getColumnByName('CLINT_HEP_UNITS')
tcClintLiver = table1.getColumnByName('CLINT_LIVER')
tcClintLiverUnits = table1.getColumnByName('CLINT_LIVER_UNITS')
tcHalfLifeMin = table1.getColumnByName('HALF_LIFE_MIN')
tcHalfLifeQualifier = table1.getColumnByName('HALF_LIFE_QUALIFIER')
tcKEliminationPerMin = table1.getColumnByName('K_ELIMINATION_PER_MIN')
tcR2 = table1.getColumnByName('R2')
tcTimeMin = table1.getColumnByName('TIME_MIN')
tcPctRemaininigTs = table1.getColumnByName('PCT_REMAININIG_TS')
tcLnPctRemaininigTs = table1.getColumnByName('LN_PCT_REMAININIG_TS')

logger.info('running script CRO_HEPATOCYTE_STAB ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    validateCompound(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatch, sheet1.getCellValue(r,1))
    row.addCell(tcStudyName, sheet1.getCellValue(r,2))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,3))
    row.addCell(tcCro, sheet1.getCellValue(r,4))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,5))
    speciesStrain = sheet1.getCellValue(r,6) + ' (' + sheet1.getCellValue(r,7) + ')'
    validateOrganismStrain(tcSpecies, speciesStrain, sheet1.getCellValue(r,6),'WARN')
    validateOrganismStrain(tcOrganismStrain, speciesStrain, sheet1.getCellValue(r,7), 'ERROR')
#    row.addCell(tcSpecies, sheet1.getCellValue(r,6))
#    row.addCell(tcOrganismStrain, sheet1.getCellValue(r,7))
    row.addCell(tcSex, sheet1.getCellValue(r,8))

    unitCheck = sheet1.getCellValue(r,9)
    row.addCell(tcClintHep, unitCheck)
    if unitCheck is not None:
        validateMissing(tcClintHepUnits, sheet1.getCellValue(r,10),'ERROR')

    unitCheck = sheet1.getCellValue(r,11)
    row.addCell(tcClintLiver,unitCheck)
    if unitCheck is not None:
        validateMissing(tcClintLiverUnits, sheet1.getCellValue(r,12) , 'ERROR')

    row.addCell(tcHalfLifeMin, sheet1.getCellValue(r,13))
    row.addCell(tcHalfLifeQualifier, sheet1.getCellValue(r,14))
    row.addCell(tcKEliminationPerMin, sheet1.getCellValue(r,15))
    row.addCell(tcR2, sheet1.getCellValue(r,16))
    row.addCell(tcTimeMin, sheet1.getCellValue(r,17))
    row.addCell(tcPctRemaininigTs, sheet1.getCellValue(r,18))
    row.addCell(tcLnPctRemaininigTs, sheet1.getCellValue(r,19))

logger.info('CRO_HEPATOCYTE_STAB script finished')