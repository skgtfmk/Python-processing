import re

start_regex = '^\d\. .*\((.*)\)'
block_label_f = '4. 4-Parameter fit based on Ratio (337 / 665 / 620)'
plate_name = '20260921 MJ CETSA Compounds ECACC Ramos Potentiation FH 8.9 Plate 1.xlsx'
regex_match = re.search(start_regex,block_label_f)

block_label = regex_match.group(1)                        
re_name = re.search('plate \d{1,2}', plate_name, re.I)
if re_name:
    plate_name = re_name.group(0)
plate_name_short = block_label + '-' + plate_name[:75-len(block_label)] + '.'

print(len(block_label), len(plate_name), len(plate_name_short), plate_name_short, regex_match.group(0) + "-" + plate_name_short)