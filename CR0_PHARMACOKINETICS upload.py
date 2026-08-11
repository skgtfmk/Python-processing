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
table1 = TableBuilder.build('CR0_PHARMACOKINETICS')

#add data block 1
data_block1 = data.addDataBlock('Block 1', table1)

#define table col names - these must match the db table col names!
tcFormattedId = table1.getColumnByName('FORMATTED_ID')
tcStudyNumber = table1.getColumnByName('STUDY_NUMBER')
tcStudyName = table1.getColumnByName('STUDY_NAME')
tcAssayDate = table1.getColumnByName('ASSAY_DATE')
tcOrganism = table1.getColumnByName('ORGANISM')
tcStrain = table1.getColumnByName('STRAIN')
tcSex = table1.getColumnByName('SEX')
tcCondition = table1.getColumnByName('CONDITION')
tcStudyType = table1.getColumnByName('STUDY_TYPE')
tcTMaxH = table1.getColumnByName('T_MAX_H')
tcTHalfH = table1.getColumnByName('T_HALF_H')
tcTHalfSdH = table1.getColumnByName('T_HALF_SD_H')
tcVDistributLKg = table1.getColumnByName('V_DISTRIBUT_L_KG')
tcVDistributSdLKg = table1.getColumnByName('V_DISTRIBUT_SD_L_KG')
tcClearanceMlMinKg = table1.getColumnByName('CLEARANCE_ML_MIN_KG')
tcClearanceSdMlMinKg = table1.getColumnByName('CLEARANCE_SD_ML_MIN_KG')
tcAucMeasured = table1.getColumnByName('AUC_MEASURED')
tcAucMeasuredSd = table1.getColumnByName('AUC_MEASURED_SD')
tcAucMeasUnits = table1.getColumnByName('AUC_MEAS_UNITS')
tcMrtH = table1.getColumnByName('MRT_H')
tcMrtSdH = table1.getColumnByName('MRT_SD_H')
tcAucBrainPlasma = table1.getColumnByName('AUC_BRAIN_PLASMA')
tcBioavailabilityPct = table1.getColumnByName('BIOAVAILABILITY_PCT')
tcFormulation = table1.getColumnByName('FORMULATION')
tcNominalDoseMgKg = table1.getColumnByName('NOMINAL_DOSE_MG_KG')
tcAdminRoute = table1.getColumnByName('ADMIN_ROUTE')
tcMatrix = table1.getColumnByName('MATRIX')
tcTimeH = table1.getColumnByName('TIME_H')
tcConcMeanNm = table1.getColumnByName('CONC_MEAN_NM')
tcConcSdNm = table1.getColumnByName('CONC_SD_NM')
tcBrainPlasmaMean = table1.getColumnByName('BRAIN_PLASMA_MEAN')
tcBrainPlasmaSd = table1.getColumnByName('BRAIN_PLASMA_SD')


logger.info('running script CR0_PHARMACOKINETICS ...')

#loop through each row in input file 
#skip first 2 header rows in this example**

for i,r in enumerate(range(1,sheet1.getNumRows(),1)):
    row = Row(i+1)
    data_block1.addRow(row)

    row.addCell(tcFormattedId, sheet1.getCellValue(r,0))
    row.addCell(tcStudyNumber, sheet1.getCellValue(r,1))
    row.addCell(tcStudyName, sheet1.getCellValue(r,2))
    row.addCell(tcAssayDate, sheet1.getCellValue(r,3))
    row.addCell(tcOrganism, sheet1.getCellValue(r,4))
    row.addCell(tcStrain, sheet1.getCellValue(r,5))
    row.addCell(tcSex, sheet1.getCellValue(r,6))
    row.addCell(tcCondition, sheet1.getCellValue(r,7))
    row.addCell(tcStudyType, sheet1.getCellValue(r,8))
    row.addCell(tcTMaxH, sheet1.getCellValue(r,9))
    row.addCell(tcTHalfH, sheet1.getCellValue(r,10))
    row.addCell(tcTHalfSdH, sheet1.getCellValue(r,11))
    row.addCell(tcVDistributLKg, sheet1.getCellValue(r,12))
    row.addCell(tcVDistributSdLKg, sheet1.getCellValue(r,13))
    row.addCell(tcClearanceMlMinKg, sheet1.getCellValue(r,14))
    row.addCell(tcClearanceSdMlMinKg, sheet1.getCellValue(r,15))
    row.addCell(tcAucMeasured, sheet1.getCellValue(r,16))
    row.addCell(tcAucMeasuredSd, sheet1.getCellValue(r,17))
    row.addCell(tcAucMeasUnits, sheet1.getCellValue(r,18))
    row.addCell(tcMrtH, sheet1.getCellValue(r,19))
    row.addCell(tcMrtSdH, sheet1.getCellValue(r,20))
    row.addCell(tcAucBrainPlasma, sheet1.getCellValue(r,21))
    row.addCell(tcBioavailabilityPct, sheet1.getCellValue(r,22))
    row.addCell(tcFormulation, sheet1.getCellValue(r,23))
    row.addCell(tcNominalDoseMgKg, sheet1.getCellValue(r,24))
    row.addCell(tcAdminRoute, sheet1.getCellValue(r,25))
    row.addCell(tcMatrix, sheet1.getCellValue(r,26))
    row.addCell(tcTimeH, sheet1.getCellValue(r,27))
    row.addCell(tcConcMeanNm, sheet1.getCellValue(r,28))
    row.addCell(tcConcSdNm, sheet1.getCellValue(r,29))
    row.addCell(tcBrainPlasmaMean, sheet1.getCellValue(r,30))
    row.addCell(tcBrainPlasmaSd, sheet1.getCellValue(r,31))

logger.info('CR0_PHARMACOKINETICS script finished')