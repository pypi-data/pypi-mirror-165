#----------------------------------------------------------------------#
# Example script for reading HIPO files
# Authors: M. McEneaney (2022, Duke University)
#----------------------------------------------------------------------#

import hipopybind as hb
import numpy as np

# Create objects for reading
r = hb.Reader()
d = hb.Dictionary()
e = hb.Event()

# Open file
filename = 'out.hipo'
r.open(filename)
r.readDictionary(d)

# Get bank structures
names = {}
types = {}
banks = {}
for treename in d.getSchemaList():
    s = d.getSchema(treename)
    b = hb.Bank(s) #NOTE: Create banks here for speed
    banks[treename] = b

    # Get bank entry names and types (as strings: 'D':double, 'F':float, 'I':int, 'S':short, 'B':byte, 'L':long)
    bankdict = None
    try:
        bankdict = d.getSchema(treename).getSchemaString()
        bankdict = bankdict.split("}{")[1][:-1]
        bankdict = { entry.split("/")[0]:entry.split("/")[1] for entry in bankdict.split(",")}
    except IndexError:
        print("schemaString unreadable")
        print("treename =",treename)
        print("schemaString =",d.getSchema(treename).getSchemaString())
    types[treename] = list(bankdict.values())
    names[treename] = list(bankdict.keys())

# Show structures
print("names =",names)
print("types =",types)

# Loop and read events
while r.next():
    r.read(e)

    # Loop banks
    for treename in banks:

        # Read in bank
        e.getStructure(banks[treename]) #NOTE: IMPORTANT! Otherwise, you get a seg fault.  Also, call for each event or you won't read any data.
        nrows = banks[treename].getRows()

        # Loop bank entries
        for idx, name in enumerate(names[treename]):

            # Read values from each entry
            t = types[treename][idx]
            values = None
            if   t=='D':
                values = [banks[treename].getDouble(name,i) for i in range(nrows)]
            elif t=='I':
                values = [banks[treename].getInteger(name,i) for i in range(nrows)]
            elif t=='F':
                values = [banks[treename].getFloat(name,i) for i in range(nrows)]
            elif t=='S':
                values = [banks[treename].getShort(name,i) for i in range(nrows)]
            elif t=='L':
                values = [banks[treename].getLong(name,i) for i in range(nrows)]
            elif t=='B':
                values = [banks[treename].getByte(name,i) for i in range(nrows)]

            # Show values
            print(name,"=",values)
