import hashlib
import sys
import os
import pickle
from bitstream import BitStream
import xml.etree.ElementTree as ET
from collections import defaultdict
from numpy import *



class Node:
    def __init__(self, freq=None, symbol=None, left=None, right=None):
        self.freq = freq # Frequency of symbol
        self.symbol = symbol # Symbol name (character)
        self.left = left # Left child 
        self.right = right # Right child 
        self.huff = '' # Binary code to specify direction for the tree traversal when decoding
        


class Huffman_coder:
    def __init__(self):
        self.dict_of_huff_codes = {} # Dictionary for storing Huffman codes
        self.nodes = [] # List for storing huffman tree_root
        self.keys = [] # Keys to huffman codes
        self.encoded_code = '' # String with Huffman codes
        self.result = []

    
    # Fill in huffman tree and a dictionary for encoding    
    def initialisation(self, text):
        
        # Get the occurrences of a character in a form of a dictionary
        occurrences = defaultdict(int)
        for char in text:
            occurrences[char] += 1
            
        symbols = occurrences.keys() # Symbols for Huffman tree
        
        # Storing characters and their frequencies into a tree
        for symbol in symbols:
            self.nodes.append(Node(occurrences.get(symbol), symbol))
        
        # Storing characters and their huffman codes in ascending order
        while len(self.nodes) > 1:
            # Sort all the nodes in ascending order based on their frequency
            self.nodes = sorted(self.nodes, key=lambda x: x.freq)
        
            # Choose 2 smallest nodes
            left = self.nodes[0]
            right = self.nodes[1]
        
            # Assign value to these nodes
            left.huff = 0
            right.huff = 1
        
            # Combine the 2 smallest nodes to create new node as their parent
            new_node = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)
        
            # Remove the 2 nodes and add their parent as new node
            self.nodes.remove(left)
            self.nodes.remove(right)
            self.nodes.append(new_node)

        self.get_huff_codes(self.nodes[0])
   
           
    # Method to get huffman codes for all symbols from the Huffman tree leaves nodes
    def get_huff_codes(self, node, val=''):
        
        # Huffman code for current node
        new_val = val + str(node.huff)
    
        # If node is not a leaf node then traverse inside it
        if(node.left):
            self.get_huff_codes(node.left, new_val)
        if(node.right):
            self.get_huff_codes(node.right, new_val)

        # If node is a leaf, then display its huffman code
        if(not node.left and not node.right):
            self.dict_of_huff_codes[node.symbol] = new_val
        return self.dict_of_huff_codes
    
    
    # Method to encode given data    
    def encode(self, text):
        
        # Calling method to fill in tree and dictionary
        self.initialisation(text)
        
        # Getting keys to huffman codes
        for k in self.dict_of_huff_codes.keys():
            self.keys += k
        
        # Writing all Huffman codes in one string  
        for c in text:
            if c in self.keys:
                self.encoded_code += self.dict_of_huff_codes.get(c)

        self.result = [self.encoded_code, self.nodes]
        
        return self.result
    
    
    # Method to decode Huffman codes into original text
    def decode(self, text, tree):
        
        tree_root = tree[0]
        node = tree_root

        decoded_data = []
        for x in text:
            if x == '0':
                node = node.left
            elif x == '1':
                node = node.right
                
            if not (node.left or node.right):
                decoded_data.append(node.symbol)
                node = tree_root
        
        # Resstored data 
        data_line = ''

        for val in decoded_data:
            data_line += val

        return data_line



class File_processor:
    
    def write_to_file(self, code, tree, file_to_write):
        
        # Representing encoded data as stream of bits 
        stream = BitStream()
        
        # Incerting leading zeros to make the number of bits multiple of 8
        # to read the data as a string from the stream
        num_of_leading_zeros = 8 - len(code) % 8
        for i in range(num_of_leading_zeros):
            stream.write(False, bool)
        
        data_len = 0
        # Writing encoded data into stream 
        for n in code:
            if n =='1':
                stream.write(True, bool)
            elif n == '0':
                stream.write(False, bool)
            data_len += 1
        
        # Reading bits from the stream by bytes
        encoded_data_bytes = stream.read(bytes)
        
        # The first byte in the file contains additional zeros
        encoded_num_of_leading_zeros = num_of_leading_zeros.to_bytes(1, 'big')
        
        # Using pickle to save the tree by serialization (creating bitstream)
        tree_string = pickle.dumps(tree)
        
        tree_len = len(tree_string)
        
        # Storing lenght of the tree within 4 bytes
        encoded_tree_len = tree_len.to_bytes(4, 'big')
        
        encoded_data_len = data_len.to_bytes(4, 'big')
        
        # Getting hush of bynary file (used to check data when decoding this file)
        hash_of_encoded_file = hashlib.md5(encoded_num_of_leading_zeros + encoded_tree_len + encoded_data_len + tree_string + encoded_data_bytes)
        
        # Create a new file (bin format) entered by user, which will content encoded data
        with open(file_to_write, "wb") as f:
            f.write(encoded_num_of_leading_zeros) # additional zeros (first byte)
            f.write(encoded_tree_len) # lenght of the tree (next 4 bytes)
            f.write(encoded_data_len) # lenght of encoded data (next 4 bytes)
            f.write(tree_string) # huffman tree of the message
            f.write(encoded_data_bytes) # encoded data
            f.write(hash_of_encoded_file.digest()) # hush of the file (last 16 bytes)
            f.close()
    
        
    def read_from_file(self, file_to_read):
        
        with open(file_to_read, "rb") as f:

            # Reading first byte
            encoded_leading_zeros_number = f.read(1) # additional zeros
            leading_zeros_number = int.from_bytes(encoded_leading_zeros_number, "big")
            
            # Reading next 8 bytes
            encoded_tree_length = f.read(4) # lenght of the tree
            encoded_data_lenght = f.read(4) # lenght of encoded data
                        
            # Converting lenght of the tree and lenght of encoded data
            # into numbers for using it later to read from the file neded info
            tree_length = int.from_bytes(encoded_tree_length, "big")
            data_lenght_bits = int.from_bytes(encoded_data_lenght, "big")
            
            encoded_tree = f.read(tree_length) # huffman tree of encoded data in bytes
            encoded_data = f.read((data_lenght_bits + leading_zeros_number) // 8) # encoded data in bytes
             
            # Get hash of this file without last 16 bytes 
            hash_of_file = hashlib.md5(encoded_leading_zeros_number + encoded_tree_length + encoded_data_lenght + encoded_tree + encoded_data)
            
            # Read hash from the file 
            hash_read = f.read()[-16:]
            
            # Compare hashes
            if not hash_of_file.digest() == hash_read:
                sys.exit ("You've entered a wrong file to decode!")
            # Restore the file
            else:
                stream = BitStream(encoded_data)
            
                restored_data = ''
                
                for i in range(data_lenght_bits + leading_zeros_number):                 
                    b = stream.read(bool)
                    if i >= leading_zeros_number:
                        if b:
                            restored_data += '1'
                        else:
                            restored_data += '0'
                
                restored_tree = pickle.loads(encoded_tree)
                
                f.close()
                
                return restored_data, restored_tree
                


class Compressor:
    
    def compress(self, file_in, file_out):

        file_to_encode = open(file_in, "r")
        
        # Read text into memory from file
        data = file_to_encode
        text = data.read()
        
        # Use Hoffman coder for encode users data
        coder = Huffman_coder()
        encoded_data = coder.encode(text)
        
        # Creating a new file with encoded information
        file_processor = File_processor()
        file_processor.write_to_file(encoded_data[0], encoded_data[1], file_out)
        
    def decompress(self, file_in, file_out):
        
        file_processor = File_processor()
        restored_data = file_processor.read_from_file(file_in)
        
        # Use Hoffman coder for decode users data
        coder = Huffman_coder()
        restored_text = coder.decode(restored_data[0], restored_data[1])
        
        # Wright encoded text to a new file
        with open(file_out, "w") as f:
            f.write(restored_text)
            f.close()



class Validator:

    def valid_to_compress(self, file_in, file_out):

        # Check whether file to compress is exist
        if os.path.exists(file_in) and not os.path.exists(file_out):
            # Check if extentions of entered files are correct
            if os.path.splitext(file_in)[1] == '.txt' and os.path.splitext(file_out)[1] == '.bin':
                compress = Compressor()
                compress.compress(file_in, file_out)
            else:
                print("Wrong extentions!")
        # Check if name for a compressed file is taken
        elif os.path.isfile(file_in) and os.path.isfile(file_out):
            # Check if extentions of entered files are correct
            if os.path.splitext(file_in)[1] == '.txt' and os.path.splitext(file_out)[1] == '.bin':
                answer = input("File for compressed data with this name already exist, would you like to overwrite it? y/n: ")
                if answer == 'y':
                    compress = Compressor()
                    compress.compress(file_in, file_out)
                else:
                    return
        else:
            print("There is no source specified.")
        
    def valid_to_decompress(self, file_in, file_out):
        # Check whether file to decompress is exist
        if os.path.isfile(file_in) and not os.path.isfile(file_out):
            # Check if extentions of entered files are correct
            if os.path.splitext(file_in)[1] == '.bin' and os.path.splitext(file_out)[1] == '.txt':
                decompress = Compressor()
                decompress.decompress(file_in, file_out)
            else:
                print("Wrong extentions!")
        # Check if name for a decompressed file is taken
        elif os.path.isfile(file_in) and os.path.isfile(file_out):
            # Check if extentions of entered files are correct
            if os.path.splitext(file_in)[1] == '.bin' and os.path.splitext(file_out)[1] == '.txt':
                answer = input("File for decompressed data with this name already exist, would you like to overwrite it? y/n: ")
                if answer == 'y':
                    decompress = Compressor()
                    decompress.decompress(file_in, file_out)
                else:
                    return
        else:
            print("There is no source specified.")



def main():
    
    # Ensure correct usage
    if len(sys.argv) != 4:
        if len(sys.argv) == 0 or (len(sys.argv) == 1 and (sys.argv[1] == '?' or sys.argv[1])) == 'help':
            sys.exit("The script requires the following parameters to be launched:\
                    - action to do: compress|decompress;\
                    - input file (*.txt for compress and *.bin for decompress)\
                    - output file (*.bin for compress and *.txt for decompress)")            
        else:        
            sys.exit("Incorrect number of paramethers.")
    
    action = sys.argv[1]
    file_to_code = sys.argv[2]
    coding_result_file = sys.argv[3]
     
    compress_command = 'compress'
    decompress_command = 'decompress'
    
    # If user choose to compress a file
    if action == compress_command:
        valid = Validator()
        valid.valid_to_compress(file_to_code, coding_result_file)
    # If user choose to decompress a file
    elif action == decompress_command:
        valid = Validator()
        valid.valid_to_decompress(file_to_code, coding_result_file)   
    # If user had make a mistake when write an action
    else:
        print("You have to choose an action. The possible actions are 'compress', 'decompress'")
    
    
 
    
if __name__ == "__main__":
    main()