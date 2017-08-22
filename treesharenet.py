from networktree import *
import random

class Node:
    """A network node
    """
    MAX_DESCENDANTS = 10
    networkAccess = NetworkTree  # Someday we will put here internet.

    def __init__(self):
        self.parentAddr = None
        self.parentSiblings = []    # fallback in case parent disapears
        self.__descendantsAddr = []
        self.__files = NetworkTree.getSomeRandomFiles()   # our hard-disk
        NetworkTree.appendNodeToNewkork( self )
        # print("New node created: ", self)

    def __str__(self): return str( str(self.address) + "=>" + str(self.__descendantsAddr))

    def getDescendants(self): return self.__descendantsAddr  # only for testing.  TODO: disable
    
    def insertNode( self, requesterAddr, node):
        """ Another node ask us to accomodate this node in a new place.
            Note that we don't now wether it is new or have descendants.
        """
        assert node.address != self.parentAddr
        assert node.address != self.address
        assert requesterAddr != self.address
        assert node.address not in self.__descendantsAddr

        if self.addDescendant( node): return True                   # Try to add the node as my direct descendant 

        if self.parentAddr and requesterAddr != self.parentAddr:    # If not ask the parent to insert it somewhere up in the tree
            conn = self.networkAccess.connectTo( self.address, self.parentAddr)
            if conn.insertNode( node): return True

        for descendant in self.__descendantsAddr:                   #  If not, ask all descendants to add it as a direct descendant (one level below only)
            if descendant == requesterAddr: continue
            conn = self.networkAccess.connectTo( self.address, descendant)
            if conn.addDescendant( node): return True

        for descendant in self.__descendantsAddr:                   # If not, then ask to instert it recursively down the tree
            if descendant == requesterAddr: continue
            conn = self.networkAccess.connectTo( self.address, descendant)
            if conn.insertNode( node): return True

        print("ERROR: Node couldn't be inserted; ", self.address, node.address, requesterAddr)

    def addDescendant( self, node):
        """ Just try to add as a direct descendant, not recursively up or down
        """
        if len( self.__descendantsAddr) < self.MAX_DESCENDANTS: # check if we have room to add it as a new descendant
            node.parentAddr = self.address
            self.__descendantsAddr.append( node.address)
            # print("  Inserted as descendant of " + str(self))
            return True
        return False

    def printSubTree( self, level):  # just for testing. TODO: remove
        print( " "*level + "-" + str( self))
        for n in self.__descendantsAddr:
            self.networkAccess.getNode(n).printSubTree(level+1)   


    ############################## SEARCH #######################################

    def searchByTitle( self, requesterAddr, searchTerm ):
        assert (requesterAddr == self.address or requesterAddr in self.__descendantsAddr 
            or requesterAddr==self.parentAddr), "Search only accepted from parent or descendants"
        result = {}
        for hashKey in self.__files:
            for f in self.__files[hashKey]:
                if searchTerm in f['title']:
                    result[hashKey] = [f]
                    break
        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.networkAccess.connectTo( self.address, descendant)
            for k,v in conn.sendSearchByTitle( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]

        if self.parentAddr and self.parentAddr != requesterAddr:
            conn = self.networkAccess.connectTo( self.address, self.parentAddr)
            for k,v in conn.sendSearchByTitle( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
        return result

    def searchByHash( self, requesterAddr, searchTerm ):
        assert (requesterAddr == self.address or requesterAddr in self.__descendantsAddr 
            or requesterAddr==self.parentAddr), "Search only accepted from parent or descendants"
        result = {}
        if searchTerm in self.__files:
            result[searchTerm] = self.__files[searchTerm]
            print( "result", result)
            
        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.networkAccess.connectTo( self.address, descendant)
            for k,v in conn.sendSearchByHash( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]

        if self.parentAddr and self.parentAddr != requesterAddr:
            conn = self.networkAccess.connectTo( self.address, self.parentAddr)
            for k,v in conn.sendSearchByHash( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
        return result


    def userSearch( self, searchTerm):
        return self.searchByTitle( self.address, searchTerm)



Node() # this initializes our internet with a 1st node
for i in range(1, 1000):
    entryPoint = NetworkTree.getRandomAddress()
    me = Node()
    conn = NetworkTree.connectTo( me.address, entryPoint)
    conn.insertNewNode( me)

# NetworkTree.printTree()

# for k,v in NetworkTree.hashes.items():
#     for t in v:
#         if 'terra tres' in t:
#             print(k, t, len(v))
#             break

entryPoint = NetworkTree.getRandomAddress()
me = Node()
conn = NetworkTree.connectTo( me.address, entryPoint)
conn.insertNewNode( me)
res = me.userSearch( 'terra t')
for r in res: print(res[r])
hashToFind = list(res.keys()).pop()
print("hashToFind", hashToFind, res[hashToFind])
me.searchByHash( me.address, hashToFind)
    