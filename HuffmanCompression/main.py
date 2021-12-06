import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# A Huffman Tree Node
class Node:
	def __init__(self, freq, symbol, left=None, right=None):
		self.freq = freq
		self.symbol = symbol
		self.left = left
		self.right = right
		self.huff = ''

class HuffmanTree:
    def __init__(self, values: dict) -> None:
        self.values = values
        self.root = None
        self.nodes = []
        self.encoded = {}
        self.DEFAULT_VALUE_NODE = chr(5)
        self.DEFAULT_VALUE = chr(6)
        self.HEADER_ESCAPE = chr(7)
        self.header = ''

        if values:
            self.build()
            self.encode()

    
    def build(self) -> None:
        logger.info("Building Huffman Tree")

        self._fillNodes()
        self.root = self._buildTree(self.nodes)

    def _fillNodes(self) -> None:
        logger.info("Filling Nodes")

        for key, value in self.values.items():
            self.nodes.append(Node(value, key))

    def _buildTree(self, nodes: list) -> Node:
        logger.info("Building Tree")

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.freq)

            left = nodes[0]
            right = nodes[1]

            left.huff = 0
            right.huff = 1

            newNode = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)

            nodes.remove(left)
            nodes.remove(right)
            nodes.append(newNode)
        return nodes[0]

    @staticmethod
    def readFile(fileName: str) -> dict:
        logger.info("Reading File")

        arr = {}
        chars = 0

        with open(fileName, encoding = 'utf-8') as file:
            for line in file:
                for char in line:
                    if char in arr:
                        arr[char] = arr[char] + 1
                    else:
                        arr[char] = 1
                    chars += 1

        for key, value in arr.items():
            arr[key] = value / chars
        
        return arr

    def encode(self) -> None:
        logger.info("Encoding")

        self._encode(self.root, '')

    def _encode(self, node: Node, val='') -> None:
        newVal = val + str(node.huff)
        print(node.symbol)

        if node.left:
            node.left.huff = '0'
            newVal = val + str(node.huff)
            self._encode(node.left, newVal)
        if node.right :
            node.right.huff = '1'
            newVal = val + str(node.huff)
            self._encode(node.right, newVal)

        if (not node.left and not node.right and len(node.symbol) == 1) or len(node.symbol) == 1:
            self.encoded[node.symbol] = newVal

    def printEncoded(self) -> None:
        logger.info("Printing Encoded Chars") 
        logger.info(self.encoded)

    def _getFileText(self, fileName: str) -> str:
        logger.info("Getting File Text")

        with open(fileName, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _encryptFileText(self, fileText: str) -> str:
        logger.info("Encrypting File Text")

        encrypted = ''
        for char in fileText:
            encrypted += self.encoded[char]

        return encrypted

    def _toBytes(self, data: str) -> bytes:
        logger.info("Converting to Bytes")

        b = bytearray()
        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2))

        return bytes(b)

    def writeFileEncrypted(self, source: str, target: str) -> None:
        logger.info("Writing File Encrypted")

        with open(target, 'wb') as file:
            logger.info("Writing Header")
            file.write(self._toBytes(self._createHeader().encode()))

            logger.info("Writing Encoded Chars")
            encrypted = self._encryptFileText(self._getFileText(source))
            
            pad = str((8 - len(encrypted) % 8)) + self.HEADER_ESCAPE
            p = ''
            for c in pad:
                p += "{0:b}".format(ord(c)).zfill(8)

            file.write(self._toBytes(p.encode()))

            encrypted += (8 - len(encrypted) % 8) * '1'
            encrypted = self._toBytes(encrypted)
            
            logger.info("Saving file")
            file.write(encrypted)

    def _createHeader(self) -> str:
        logger.info("Creating Header")

        self.header = ''
        self._traverseDown(self.root)
        self.header += self.HEADER_ESCAPE

        encoded = ''
        for c in self.header:
            encoded += "{0:b}".format(ord(c)).zfill(8)

        return encoded
        
    def _traverseDown(self, node: Node, val='') -> str:
        if node is None:
            #self.header += self.DEFAULT_VALUE
            return
        else:
            if len(node.symbol) == 1:
                self.header += node.symbol
            else:
                self.header += self.DEFAULT_VALUE_NODE

            self._traverseDown(node.left, val)
            self._traverseDown(node.right, val)

    def _traverseUp(self) -> Node:
        if self.header == '':
            return None

        val = self.header[0]
        self.header = self.header[1:]

        if val != self.DEFAULT_VALUE_NODE and val != self.DEFAULT_VALUE :
            #self.header = self.header[2:]
            return Node(0, val)
        else:
            node = Node(0, val*2)
            node.left = self._traverseUp()
            node.right = self._traverseUp()
            return node

        #print(self.header)
        # FIXME: i dont know but this does not work
        # if self.header == '':
        #     return None
        # else:
        #     node = Node(0, 'aa')
        #     if self.header[0] == self.DEFAULT_VALUE_NODE:
        #         node.symbol = self.DEFAULT_VALUE_NODE * 3    
        #     elif self.header[0] == self.DEFAULT_VALUE:
        #         node.symbol = self.DEFAULT_VALUE * 3
        #     else:
        #         node.symbol = self.header[0]
        #     self.header = self.header[1:]
        #     node.left = self._traverseUp()
        #     node.right = self._traverseUp()
        #     return node

    def _readEncrypted(self, fileName: str) -> bytes:
        logger.info("Reading Encrypted File")

        with open(fileName, 'rb') as file:
            encrypted = file.read()

        return encrypted

    def _reverse_encoding(self, content: bytes, pad: int) -> str:
        logger.info("Reverse Encoding")

        decoded = ''
        for c in content:
            decoded += "{0:b}".format(c).zfill(8)

        decoded = decoded[:-pad]

        value = ''
        tmp = ''
        for b in decoded:
            tmp += b
            if tmp in self.encoded.values():
                value += list(self.encoded.keys())[list(self.encoded.values()).index(tmp)]
                tmp = ''
            
        return value 

    def writeFileDecrypted(self, source:str, target:str) -> None:
        logger.info("Writing File Decrypted")

        data = self._readEncrypted(source)

        logger.info("Decrypting Header")
        self.header = ''
        for b in data:
            c = chr(b)
            if c == self.HEADER_ESCAPE:
                break
            self.header += c
        
        #self.header = self.header[1:]
        data = data[(len(self.header)+1):]
        self.root = Node(0, 'aa')
        self.root = self._traverseUp()
        self.encode()

        self.printEncoded()

        pad = ''
        for b in data:
            c = chr(b)
            if c == self.HEADER_ESCAPE:
                break
            pad += c
        data = data[(len(pad)+1):]

        logger.info("Decrypting Encoded Chars")
        decoded = self._reverse_encoding(data, int(pad))

        logger.info("Saving to File")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(decoded)

def compareLength(source: str, target: str) -> None:
    logger.info("Comparing Length")

    with open(source, 'rb') as file:
        source = file.read()

    with open(target, 'rb') as file:
        target = file.read()

    logger.info("Source: " + str(len(source)))
    logger.info("Target: " + str(len(target)))
    logger.info("Compression: " + str(len(target)/len(source)))

def encodeFile(source: str, target: str) -> None:
    values = HuffmanTree.readFile(source)
    tree = HuffmanTree(values)
    tree.printEncoded()
    tree.writeFileEncrypted(source, target)

def decodeFile(source: str, target: str) -> None:
    tree = HuffmanTree(None)
    tree.writeFileDecrypted(source, target)

# Commandline execution for functions encodeFile and decodeFile and compareLength with the same arguments
import sys

def main():
    if len(sys.argv) == 4:
        if sys.argv[1] == '-e':
            encodeFile(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == '-d':
            decodeFile(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == '-c':
            compareLength(sys.argv[2], sys.argv[3])
        else:
            print("Invalid command")
    else:
        print("Invalid number of arguments")

if __name__ == '__main__':
    #main()
    encodeFile('test.txt', 'test.huff')
    decodeFile('test.huff', 'test.decrypted')
