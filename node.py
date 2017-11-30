from networktree import *
import random, math

class Node:
    """A network node
    """
    MAX_DESCENDANTS = 4
    networkAccess = NetworkTree  # Someday we will put here internet.

    def __init__(self):
        self.parentAddr = None
        self.parentSiblings = []    # fallback in case parent disapears
        self.__descendantsAddr = []
        self.__files = NetworkTree.getSomeRandomFiles()   # our hard-disk
        self.address = None
        NetworkTree.appendNodeToNewkork( self )
        # print("New node created: ", self)

    def __str__(self): return str( str(self.address) + " => " + str(self.__descendantsAddr))

    def getDescendants(self): return self.__descendantsAddr  # only for testing.  TODO: disable 

    def __connectTo( self, toAddr):
        return self.networkAccess.connectTo( self.address, toAddr)
    
    def insertNode( self, requesterAddr, node):
        """ Another node ask us to accomodate this node in a new place.
            Note that we don't now wether it is new, leaf or have descendants.
        """
        assert node.address != self.parentAddr
        assert node.address != self.address
        assert requesterAddr != self.address
        assert node.address not in self.__descendantsAddr
        #print( self.address, "insertNode: ", node.address)
        if self.__descendantsAddr and self.addDescendant( node): return True    # Without increasing deep, try to add as direct descendant

        for descendant in self.__descendantsAddr:
            if descendant == requesterAddr: continue
            conn = self.__connectTo( descendant)
            if conn.insertNode( node): return True

        if self.parentAddr is not None and requesterAddr != self.parentAddr:    # Ask the parent to insert it somewhere up in the tree
            conn = self.__connectTo( self.parentAddr)
            if conn.insertNode( node): return True
            if conn.insertNodeDeepIncrease( node): return True

        # print("ERROR: Node couldn't be inserted.", self.address, node.address)
        return False

    def insertNodeDeepIncrease( self, node):
        lessDeepDescendant = self.getLessDeepDescendant()   # Ask the descendant with the smaller subtree
        if lessDeepDescendant is None: 
            #print(" +DEEP", self.address, node.address)
            #NetworkTree.printTree()
            return self.addDescendant( node)    # 1st descendat. Here we increase the deep of this branch
        conn = self.__connectTo( lessDeepDescendant)
        if conn.insertNodeDeepIncrease( node): return True

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
            conn = self.__connectTo( descendant)
            deeps.append( conn.getDeep())
        return (max( deeps ) + 1)

    def getLessDeepDescendant( self):
        minDesc = math.inf # infinite
        minAddr = None
        for descendant in self.__descendantsAddr:
            conn = self.__connectTo( descendant)
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
        for hashKey in self.__files:
            for f in self.__files[hashKey]:
                if searchTerm in f['title']:
                    result[hashKey] = [f]
                    break
        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.__connectTo( descendant)
            for k,v in conn.sendSearchByTitle( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
            # TODO if result has already a lot of results, stop searching and return

        if self.parentAddr is not None and self.parentAddr != requesterAddr:
            conn = self.__connectTo( self.parentAddr)
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
            
        for descendant in self.__descendantsAddr: 
            if descendant == requesterAddr: continue
            conn = self.__connectTo( descendant)
            for k,v in conn.sendSearchByHash( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
            # TODO if result has already a lot of results, stop searching and return

        if self.parentAddr is not None and self.parentAddr != requesterAddr:
            conn = self.__connectTo( self.parentAddr)
            for k,v in conn.sendSearchByHash( searchTerm).items():
                if k in result: 
                    result[k].extend(v)
                else: result[k] = v
                assert v, "result Value empty: %r" % result[k]
        return result


    def userSearch( self, searchTerm):
        return self.searchByTitle( self.address, searchTerm)

