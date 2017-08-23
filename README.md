# TreeShareNet
## At the moment this is a proof of concept of a decentralized and anonymous P2P sharing network.

Main goals are:
* No centralized servers. Any node acts as a server, relay, search provider, etc.
* Any node can anonymously:
  * share files.
  * search for files and for 'chunks' of the files
  * download files.
* It's not posible, even for multiple malicious nodes:
  * to find out who is sharing anything.
  * to find out who is searching anything.
  * to find out who is receiving anything.
* Prevent weakness by traffic analysis combined with malicious nodes should be posible to mitigate (...).

This is acomplished not by encrypting the connections but by the way of forwarding the pieces of information around. A malicious node can easily see that someone is asking for a file or is sending a piece of a file around, but there is no way to determine whether the origin or destination of the data is that node or it is just a relay of some (or many) small chunks.

The nodes are organized in k-tree structure, a tree with K nodes in each level. Each node can comunicate only with its parent and direct descendants. Responses from them come from the rest of the network behind that node. Is not posible to guess if any of the nodes around has more nodes connected, is a 'leaf' or which files is hosting or searching.  
There are some optimizations and shortcuts to avoid flooding the network without comprimising the security.

I know that there are many implementations and studies about this topics, but I don't know if this approach has been tried before. Anyway I'm doing this just for fun :-)

First goal is to create a proof of concept by a network simulation in memory.  Internet is a python array of nodes, connections are simulated, etc. Encryption is not a priority now (but can be added later). Nodes should be safe even if everything is travelling in plain text. At the end there will be always someone in the position to see the data, at least the one at the other side of the end-to-end tunnel.

If a malicious node is downloading a 'sensible' file he can easily find out the IP address of the remote node, this is something that can not be prevented with encription. But he will not be able to assure that that node is hosting the file, just that it is forwarding some chuncks.  Even if the malicious node counts all chuncks and stablishes that the complete file was travelling from one node, it can be just by this node caching all chuncks because of high demand, a big HD/bandwidth for caching or just by chance. Random behaviour can be introduced to prevent statistical analysis, e.g. never sending the full file to the same node, share more spread own files, etc.

So far the in-memory network has the next functionalities working:

* Insert a new node in the network, or recolocate. 
* Network always balanced (partially) with the minimum depth.
* Assign random files to each new node (random filename, content, size and hash based in the content).
* Search for a file by title.
* Search for a file by the hash out of the previous search.

Next steps:
* Request and transfer chunks with some basic optimizations.
* Modelization of a real network: adding transfer delays, processing delays, storage/bandwidth limits, etc.
* Build some in memory masive tests and measures.
* (...)
* Add real network capabilities.
* Encryption.
* ...

## Requeriments:
Python 3
## Usage
Move to the project folder and execute:  
>```python treesharenet.py```

In the prompt you can try some search over the nodes and their randomly created files.  Try with combinations of the words: *terra bosc pins*    
For example:  
> ```s terra```  

or 

> ```s terra pins```

If you get several files in a row is because the 'content' field is the same, so is the same file altough the title can be different.

Quit with *q*.



