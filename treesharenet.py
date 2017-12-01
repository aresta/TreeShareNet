from node import Node
from networktree import *

TotalNodes = 801
print("Creating test network with %r nodes." % TotalNodes)

newNode = Node( ConnectionDriver(), StorageDriver())
newNode.setFiles( StorageDriver.chooseSomeFiles())
nodes = [ newNode ]

# create a bunch of nodes and join to the TSN network
for i in range(1, TotalNodes):
    memberAddress = random.choice( nodes).address
    newNode = Node( ConnectionDriver(), StorageDriver())
    newNode.setFiles( StorageDriver.chooseSomeFiles())
    assert memberAddress != newNode.address
    newNode.requestJoinTSN( memberAddress)
print("Network created.")

me = random.choice( nodes)
print("Connected!")
print("""

Commands: 
 s [string]    search files by filename
 si [index]    search filea by index of previous search
 nodes         shows tree with nodes and descendants
 f             shows all random created files
 q             bye

  Hint, try:  s terra

""")

results = {}
bye = False
while(not bye):
    s = input("> ")
    comm = s.split()
    if len(comm) == 0: continue

    if comm[0]=='nodes':
        NetworkTree.printTree()

    elif comm[0]=='s':
        res = me.userSearch( s[ len(comm[0])+1:] )
        i=1
        results.clear()
        for r in res: 
            print(i, res[r][0]['title'], len(res[r]))
            results[i] = r
            i+=1

    elif comm[0]=='si':
        res = me.searchByHash( me.address, results[ int(comm[1]) ] )
        print( res)

    elif comm[0]=='f':
        # print(StorageDriver.worldFiles)
        for h,f in StorageDriver.worldFiles.items():
            print( h, f)
    
    elif comm[0]=='deep':
        print( NetworkTree.treeDeep())

    elif comm[0]=='q':
        print('Bye!')
        bye = True
    
