import random
import hashlib

class CONSTS:
    TESTWORDS = "En ma terra del Vallès tres turons fan una serra quatre pins un bosc espès cinc quarteres massa terra Com el Vallès no hi ha res".split()
    CHUNK_SIZE = 50

class NetworkTree:
    """ Our home-made internet
    """
    __nodes = {}
    hashes = {}
    
    def __str__(self):
        return str(NetworkTree.__nodes)

    @staticmethod
    def connectTo( fromAddr, toAddr):
        toNode = NetworkTree.__getNode(toAddr)
        return TSNConnection( fromAddr, toNode)

    @staticmethod
    def appendNodeToNewkork( newNode ): 
        newNode.address = NetworkTree.generateNewAddr()
        NetworkTree.__nodes[newNode.address] = newNode # TODO: concurrence problems (?)

    @staticmethod
    def generateNewAddr():
        return (max( NetworkTree.__nodes.keys() ) + 1) if NetworkTree.__nodes else 1

    @staticmethod
    def __getRoot(): # only for testing. TODO: disable
        for n in NetworkTree.__nodes:
            if NetworkTree.__getNode(n).parentAddr is None:
                return NetworkTree.__getNode(n)
        return None

    @staticmethod
    def __getNode( addr): 
        assert addr in NetworkTree.__nodes, "getnode: address not in network: %r" % addr
        return NetworkTree.__nodes[addr] # only for testing. TODO: disable

    @staticmethod
    def getRandomAddress(): # only for testing. TODO: disable
        return random.choice( list( NetworkTree.__nodes.keys()))

    @staticmethod
    def hashString( s ):
        hash_object = hashlib.sha256( s.encode('utf-8'))
        return hash_object.hexdigest()

    #### For testing #####

    @staticmethod
    def treeDeep():
        return NetworkTree.__getRoot().getDeep()

    @staticmethod
    def printTree():
        NetworkTree.printSubTree( NetworkTree.__getRoot(), 0)

    @staticmethod
    def printSubTree( node, level ):
        descendants = node.getDescendants()
        if not descendants: return 
        print( "  "*level + str( node.address) + "\\")
        for n in descendants:
            print( "  "*(level+1) + str(NetworkTree.__getNode(n)))
        for n in descendants:
            NetworkTree.printSubTree( NetworkTree.__getNode(n), level+1) 

    @staticmethod
    def getSomeRandomFiles():
        result = {}
        for i in range(3, random.randint(0,10)):
            title = " ".join( random.sample( CONSTS.TESTWORDS, 4))
            content = " ".join( random.sample( CONSTS.TESTWORDS, 2))
            size = random.randint(100,10000)
            newFile = {'title': title, 'content': content, 'size': size, 'chunks':size/CONSTS.CHUNK_SIZE}
            hashKey = NetworkTree.hashString(content)
            if hashKey in result: result[hashKey].append(newFile) 
            else: result[hashKey] = [newFile]
            if hashKey in NetworkTree.hashes: NetworkTree.hashes[hashKey].append(newFile)
            else: NetworkTree.hashes[hashKey] = [newFile]
        return result

class TSNConnection:
    """ Nodes comunication inteface
    """

    def __init__( self, fromAddr, toNode):
        self.fromAddr = fromAddr
        self.toNode = toNode

    def insertNode( self, node ):
        return self.toNode.insertNode( self.fromAddr, node)

    def insertNodeDeepIncrease( self, node ):
        return self.toNode.insertNodeDeepIncrease( node)

    def insertNewNode( self, newNode): 
        if self.toNode.insertNode( self.fromAddr, newNode): return True
        return self.toNode.insertNodeDeepIncrease( newNode)

    def addDescendant( self, newNode ):
        return self.toNode.addDescendant( newNode)
    
    def sendSearchByTitle( self, searchTerm):
        return self.toNode.searchByTitle( self.fromAddr, searchTerm)
    
    def sendSearchByHash( self, searchTerm):
        return self.toNode.searchByHash( self.fromAddr, searchTerm)

    def getDeep( self):
        return self.toNode.getDeep()
    

    



