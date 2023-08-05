#----------------------------------------------------------------------#
# Example script for writing HIPO files
# Authors: M. McEneaney (2022, Duke University)
#----------------------------------------------------------------------#

import hipopybind as hb
import numpy as np

# Create objects for writing
w = hb.Writer()
d = hb.Dictionary()
e = hb.Event()

# Create schema and add
treename = 'tree'
group = 1
item = 1
schemastring = 'px/D,py/D,pz/D,e/D'
s = hb.Schema(treename,group,item)
s.parse(schemastring)
print("schema s = ",s)
d.addSchema(s)
w.addDictionary(d)

# Open file
filename = 'out.hipo'
w.open(filename)

# Create bank
b = hb.Bank(d.getSchema(treename))
e.getStructure(b) #NOTE: IMPORTANT! Otherwise, you get a seg fault.

# Bank fill loop
names = ['px','py','pz','e']
nevents = 3
nrows = 1
for i in range(nevents):
    b.reset() #NOTE: IMPORTANT! Data gets transposed for some reason if you flip to higher rows.
    b.setRows(nrows)
    for row in range(nrows):
        for name in names:
            value = np.random.random()
            b.putDouble(name,row,value)

    # Show bank data
    print("Iteration",i)
    print(b)

    # Add data to event and add event to writer...
    e.reset() #NOTE: IMPORTANT! Otherwise you just write the same event over and over.
    e.addStructure(b)
    w.addEvent(e)

# Bank fill loop with vectors
names = ['px','py','pz','e']
nevents = 3
nrows = 3
for i in range(nevents):
    b.reset() #NOTE: IMPORTANT! Data gets transposed for some reason if you flip to higher rows.
    b.setRows(nrows)
    for name in names:
        values = np.random.random(size=(nrows,))
        b.putDoubles(name,values)

    # Show bank data
    print("Iteration",i)
    print(b)

    # Add data to event and add event to writer...
    e.reset() #NOTE: IMPORTANT! Otherwise you just write the same event over and over.
    e.addStructure(b)
    w.addEvent(e)
    
# Close file
w.close()
