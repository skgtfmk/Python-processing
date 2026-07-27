
import re
import datetime
import openpyxl

def find_Plate_ID (fContents):
    current_r =0
    all_found = False
    lPlate_Id = ''
    lPlate_date = ''
    while current_r < max_row :

        re_prop = re.search('ID(\d):\s*(.+?)\s*$',','.join(fContents[current_r]))
        if re_prop:
    #       logger.info(re_prop.group(1), re_prop.group(2))
            try:
                if re_prop.group(1) == '1':
                    lPlate_Id = re_prop.group(2)
                elif re_prop.group(1) == '3':
                    lPlate_date = re_prop.group(2)
            except:
                lPlate_Id = 'Plate ' + str(plate_n)
                lPlate_date = datetime.datetime.now()
    #        logger.info('Plate name = ' + plate_id + 'Date =' + str(plate_date))
        logger.info(current_r, fContents[current_r][0])
        re_prop = re.search('Protocol File Name .*\\(.+\\)*(.+)\.(.+)$',fContents[current_r][0])
        if re_prop:
            lPlate_Id = re_prop.group(2)
            logger.info("Plate ID is " + lPlate_Id)
        re_prop = re.search('Start Date.*= (.*)',fContents[current_r][0])
        if re_prop:
            lPlate_date = re_prop.group(1)
            logger.info("Start date = ", lPlate_date)
        if (lPlate_Id != '' and lPlate_date != ''): break
    return lPlate_Id, lPlate_date

fPath = 'C:\\Users\\skgtfmk\OneDrive - University College London\\Documents\\Requests information\\B-Score plate correction\\FLIPR'
fFile = '12032025_03 dec 2025 -EAAT2 -CNS library  AM plate 1_n001.statAll.xlsx'
df = openpyxl.load_workbook(fPath + '\\' + fFile)
max_row = df['12032025_03 dec 2025 -EAAT2 -CN'].max_row
print(df['12032025_03 dec 2025 -EAAT2 -CN'])
plate_id, plate_date = find_Plate_ID(df['12032025_03 dec 2025 -EAAT2 -CN'])