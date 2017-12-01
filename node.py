from networktree import *
import random, math

class Node:
    """A network node
    """
    MAX_DESCENDANTS = 4

    def __init__(self, connectionDriver, storageDriver):
        self.__connectionDriver = connectionDriver  # Someday we will put here internet.
        self.__storageDriver = storageDriver        # our hard-disk
        self.parentAddr = None
        self.parentSiblings = []    # fallback in case parent disapears
        self.__descendantsAddr = []
        self.address = None
        NetworkTree.appendNodeToNewkork( self )
        self.__connectionDriver.fromAddr = self.address
        # print("New node created: ", self)

    def __str__(self): return str( str(self.address) + " => " + str(self.__descendantsAddr))

    def setFiles( self, files ):
        self.files = files

    def getDescendants(self): return self.__descendantsAddr  # only for testing.  TODO: disable 

    def requestJoinTSN(self, memberAddress): 
        conn = self.__connectionDriver.connectTo( memberAddress)
        conn.insertNode( self)

    def insertNode( self, requesterAddr, node):
        """ Another node ask us to accomodate this node in a new place.
            Note that we don't now wether it is new, leaf or have descendants.
        """
        assert node.address != self.parentAddr
        assert node.address != self.address
        assert requesterAddr != self.address
        assert node.address not in self.__descendantsAddr
        #print( "insertNode: ", self, node)
        if self.__descendantsAddr and self.addDescendant( node): return True    # Without increasing deep, try to add as direct descendant

        for descendant in self.__descendantsAddr:
            if descendant == requesterAddr: continue
            conn = self.__connectionDriver.connectTo( descendant)
            if conn.insertNode( node): return True

        if self.parentAddr is not None and requesterAddr != self.parentAddr:    # Ask the parent to insert it somewhere up in the tree
            conn = self.__connectionDriver.connectTo( self.parentAddr)
            if conn.insertNode( node): return True
            if conn.insertNodeDeepIncrease( node): return True

        if self.parentAddr is None:
            return self.insertNodeDeepIncrease( node)
        return False

    def insertNodeDeepIncrease( self, node):
        lessDeepDescendant = self.getLessDeepDescendant()   # Ask the descendant with the smaller subtree
        if lessDeepDescendant is None: 
            #print(" +DEEP", self.address, node.address)
            #NetworkTree.printTree()
            return self.addDescendant( node)    # 1st descendat. Here we increase the deep of this branch
        conn = self.__connectionDriver.connectTo( lessDeepDescendant)
        return conn.insertNodeDeepIncrease( node)

    def addDescendant( self, node):
        """ Just try to add as a direct descendant, not recursively up or down
        """
        if len( self.__descendantsAddr) < self.MAX_DESCENDANTS: # check if we have room to add it as a new descendant
            node.parentAddr = self.address
            self.__descendantsAddr.append( node.address)
            return True
        return False

    def getDeep( self):
        deeps = []
        if not self.__descendantsAddr: return 1
        for descendant in self.__descendantsAddr:
            conn = self.__connectionDriver.connectTo( descendant)
            deeps.append( conn.getDeep())
        return (max( deeps ) + 1)

    def getLessDeepDescendant( self):
        minDesc = math.inf # infinite
        minAddr = None
        for descendant in self.__descendantsAddr:
            conn = self.__connectionDriver.connectTo( descendant)
            d = conn.getDeep()
            if d < minDesc:
                minDesc = d
                minAddr = descendant
        return minAddr
             


    ############################## SEARCH #######################################

    def searchByTitle( self, requesterAddr, searchTerm ):
        assert (requesterAddr == self.address or requesterAddr in self.__descendantsAddr 
            or requesterAddr==self.parentAddr), "Search only accepted from parent or descendants"
        result = {}
        for hashKey, file in self.files.items():
            if searchTerm in file['title']:
                result[hashKey] = [file]
                break
        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.__connectionDriver.connectTo( descendant)
            for k,v in conn.sendSearchByTitle( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
            # TODO if result has already a lot of results, stop searching and return

        if self.parentAddr is not None and self.parentAddr != requesterAddr:
            conn = self.__connectionDriver.connectTo( self.parentAddr)
            for k,v in conn.sendSearchByTitle( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
        return result

    def searchByHash( self, requesterAddr, hash ):
        assert (requesterAddr == self.address or requesterAddr in self.__descendantsAddr 
            or requesterAddr==self.parentAddr), "Search only accepted from parent or descendants"
        result = []
        if hash in self.files:
            result.append( self.files[hash])

        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.__connectionDriver.connectTo( descendant)
            result += conn.sendSearchByHash( hash)
            # TODO if result has already a lot of results, stop searching and return

        if self.parentAddr is not None and self.parentAddr != requesterAddr:
            conn = self.__connectionDriver.connectTo( self.parentAddr)
            result += conn.sendSearchByHash( hash)
        return result

    def userSearch( self, searchTerm):
        return self.searchByTitle( self.address, searchTerm)




