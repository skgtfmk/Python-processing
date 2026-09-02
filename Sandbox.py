def validateCompound(testValue):
    if testValue[0:4] == 'ARUK':
        return ' is an ARUK DDI number'
    else:
        return ' is unknown'

compoundList = ['ARUK3007277', 'SM-450']
for myCompound in compoundList:
    identification = validateCompound(myCompound)
    print (myCompound + identification)