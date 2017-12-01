import random, math
import hashlib

class NetworkTree:
    """ Our home-made internet
    """
    __nodes = {}
    
    def __str__(self):
        return str(NetworkTree.__nodes)

    @staticmethod
    def connectTo( fromAddr, toAddr):
        toNode = NetworkTree.__getNode(toAddr)
        return Connection( fromAddr, toNode)

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





    #################### For testing #####################

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
        descNodes = [NetworkTree.__getNode(n) for n in descendants]
        desc2 = [n.getDescendants() for n in descNodes]
        if( not any( desc2)): return
        print( "\t"*level + "     " + str( node.address) + "\\")
        for d in descNodes:
            print( "\t"*(level+1) + str(d))
        for d in descNodes:
            NetworkTree.printSubTree( d, level+1) 





############################################################################
############################ Environment Classes ############################

class ConnectionDriver:
    """ Inteface to access the other nodes
    """
    fromAddr = None
    def connectTo( self, toAddr):
        return NetworkTree.connectTo( self.fromAddr, toAddr)


class Connection:
    """ A connection between two nodes
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
    

class StorageDriver:

    worldFiles = None

    def __init__( self):
        if StorageDriver.worldFiles is not None: return
        StorageDriver.worldFiles = {}
        for i in range(1, 100):
            title = " ".join( random.sample( CONSTS.TESTWORDS, 5))
            content = " ".join( random.sample( CONSTS.TESTWORDS, 25))
            size = len(content) * 10000
            newFile = {'title': title, 'content': content, 'size': size, 'chunks': math.ceil( size/CONSTS.CHUNK_SIZE)}
            hashKey = StorageDriver.hashString(content)
            StorageDriver.worldFiles[hashKey] = newFile
    
    @staticmethod
    def hashString( s ):
        hash_object = hashlib.sha256( s.encode('utf-8'))
        return hash_object.hexdigest()

    @staticmethod
    def chooseSomeFiles():
        hashes = random.sample( list( StorageDriver.worldFiles), 5)
        files = {}
        for h in hashes:
            files[h] = StorageDriver.worldFiles[h]
        return files
        
    
class CONSTS:
    CHUNK_SIZE = 50
    TESTWORDS = """
Una nit de lluna plena
tramuntarem la carena
lentament, sense dir re.
Si la lluna feia el ple
tambe el feu la nostra pena.
L'estimada m'acompanya
de pell bruna i aire greu
(com una marededeu
que han trobat a la muntanya).
Perque ens perdoni la guerra,
que l'ensagna, que l'esguerra,
abans de passar la ratlla,
m'ajec i beso la terra
i l'acarono amb l'espatlla.
A Catalunya deixi
el dia de ma partida
mitja vida condormida;
l'altra meitat vingue amb mi
per no deixar-me sens vida.
Avui en terres de França
i dema mes lluny potser,
no em morire d'enyorança
ans d'enyorança viure.
En ma terra del valles
tres turons fan una serra,
quatre pins un bosc espes,
cinc quarteres massa terra.
Com el valles no hi ha res.
Que els pins cenyeixin la cala,
l'ermita dalt del pujol;
i a la platja un tenderol
que bategui com una ala.
Una esperança desfeta,
una recança infinita.
I una patria tan petita
que la somio completa.
""".split()

