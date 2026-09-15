import re

start_regex = '^\d\. .*\((.*)\)'
block_label_f = '4. 4-Parameter fit based on Ratio (337 / 665 / 620)'
plate_name = 'ECACC cells compounds tested in potentiation mode EC65 6 ugmL in columns 2 and 47 and across plate emax columns 28 and 29'
regex_match = re.search(start_regex,block_label_f)

block_label = regex_match.group(1)                        
plate_name_short = block_label + '-' + plate_name[:99-len(block_label)]

print(len(block_label), len(plate_name), len(plate_name_short), plate_name_short)