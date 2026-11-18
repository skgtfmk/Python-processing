from com.dotmatics.dataig.studies.dataparser.processor import ExcelFileProcessor
from com.dotmatics.dataig.studies.dataparser.builder import TableBuilder
from com.dotmatics.dataig.studies.dataparser.data import Row
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

#    logger.info ('Project ID is ' + str(projectId) + ', Datasource key is ' + dataSourceKeys + ' Test value is ' + testValue)
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
#            logger.info('Got to the Convert part')
            returnValue = supplier_map.getDataSources()['1167']['1']['FORMATTED_ID']
#    logger.info('ARUK number for ' + testValue + ' is ' + str(returnValue))

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
table1 = TableBuilder.build('CRO_MICROSOMAL_STAB')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcBatch = table1.getColumnByName('BATCH')
tcCro = table1.getColumnByName('CRO')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcSpecies = table1.getColumnByName('SPECIES')
tcClintMicQual = table1.getColumnByName('CLINT_MIC_QUAL')
tcClintMic = table1.getColumnByName('CLINT_MIC')
tcClintMic_Units = table1.getColumnByName('CLINT_MIC_UNITS')
tcClintLiverQual = table1.getColumnByName('CLINT_LIVER_QUAL')
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
tcOrganismStrain = table1.getColumnByName('ORGANISM_STRAIN')
tcMicrosomeConc = table1.getColumnByName('MICROSOME_CONC')
tcMicrosomeConcUnit = table1.getColumnByName('MICROSOME_CONC_UNIT')

logger.info('running script CRO_MICROSOMAL_STAB ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    validateCompound(tcFormattedId, sheet1.getCellValue(r,0))
#    row.addCell(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcBatch, sheet1.getCellValue(r,1))
    row.addCell(tcCro, sheet1.getCellValue(r,2))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,3))
    row.addCell(tcSpecies, sheet1.getCellValue(r,4))
    row.addCell(tcClintMicQual, sheet1.getCellValue(r,5))
    row.addCell(tcClintMic, sheet1.getCellValue(r,6))
    row.addCell(tcClintMic_Units, sheet1.getCellValue(r,7))
    row.addCell(tcClintLiverQual, sheet1.getCellValue(r,8))
    row.addCell(tcClintLiver, sheet1.getCellValue(r,9))
    row.addCell(tcClintLiver_Units, sheet1.getCellValue(r,10))
    row.addCell(tcHalfLife_Qualifier, sheet1.getCellValue(r,11))
    row.addCell(tcHalfLife_Min, sheet1.getCellValue(r,12))
    row.addCell(tcR2, sheet1.getCellValue(r,13))
    row.addCell(tcWcfRemaining_60Min, sheet1.getCellValue(r,14))
    row.addCell(tcNcfRemaining_60Min, sheet1.getCellValue(r,15))
    row.addCell(tcKElimination_Per_Min, sheet1.getCellValue(r,16))
#    row.addCell(tcUploadDate, sheet1.getCellValue(r,15))
    row.addCell(tcTimeMin, sheet1.getCellValue(r,18))
    row.addCell(tcPctRemaininig_Ts, sheet1.getCellValue(r,19))
    row.addCell(tcLnPct_Remaininig_Ts, sheet1.getCellValue(r,20))
    row.addCell(tcStudyName, sheet1.getCellValue(r,21))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,22))
    row.addCell(tcOrganismStrain, sheet1.getCellValue(r,23))
    row.addCell(tcMicrosomeConc, sheet1.getCellValue(r,24))
    row.addCell(tcMicrosomeConcUnit, sheet1.getCellValue(r,25))

logger.info('CRO_MICROSOMAL_STAB script finished')