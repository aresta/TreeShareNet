from node import Node
from networktree import *

TotalNodes = 1001
print("Creating test network with %r nodes." % TotalNodes)
Node() # this initializes our internet with a 1st node

for i in range(1, TotalNodes):
    entryPoint = NetworkTree.getRandomAddress()
    me = Node()
    assert entryPoint != me.address
    conn = NetworkTree.connectTo( me.address, entryPoint)
    conn.insertNewNode( me)
print("Network created.")

entryPoint = NetworkTree.getRandomAddress()
me = Node()
conn = NetworkTree.connectTo( me.address, entryPoint)
conn.insertNewNode( me)
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
            print(i, res[r])
            results[i] = r
            i+=1

    elif comm[0]=='si':
        res = me.searchByHash( me.address, results[ int(comm[1]) ] )
        print( res)

    elif comm[0]=='f':
        for h in NetworkTree.hashes: 
            print( NetworkTree.hashes[h])
    
    elif comm[0]=='deep':
        print( NetworkTree.treeDeep())

    elif comm[0]=='q':
        print('Bye!')
        bye = True
    
