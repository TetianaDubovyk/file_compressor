# Python text files compressor based on Huffman's compression algorithm
The usage of the compressor is reasonable for compression of large text files
#### Video Demo:  <URL HERE>
## Table of Contents

* [How to use it](#how-to-use-it)
* [How does it work](#how-does-it-work)
  * [Compress](#compress)
  * [Decompress](#decompress)
* [About the algorithm](#about-the-algorithm)
* [Design of the project](#design-of-the-project)

## How to use it
The script requires the following parameters to be launched: 

 ```
 python text_file_copmressor.py compress FILE.txt FILE.bin
```
 ```
 python text_file_copmressor.py decompress FILE.bin FILE.txt
```
 
## How does it work
 ### Compress
 The user calls the script providing following parameters: 
 * "compress" for an action
 * "*.txt" file to compress 
 * "*.bin" file to store compressed data in
 
 After that the validation of given files begins: if the file to compress exists and the one with compressed data does not and types of entered files are correct then the script encodes the text file into binary file which contents encoded data, some additional data and hash of a file for validation when decompressing. If output file specified already exists, then user asked for permission to overwrite it with new data.
 
 ### Decompress
 The user provides the following parameters: 
 * "decompress" for an action
 * "*.bin" file to decompress
 * "*.txt" file to store decompress data in
 
 The same validation begins, though now it also checks if given bin file is an actual file that was previously compressed. Validation compares the hash of this file content without the last 16 bytes with the hash stored within its last 16 bytes and if they match proceeds with the decompression. The result of decompression is a text file.

## About the algorithm
> Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.
The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream.  
 
More about Huffman coding on [Wikipedia, Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding#Basic_technique)

 ## Design of the project
 I've decided to use object-oriented paradigm when designing the code. After some analysis I've figured out the following classes:
 
 class Validator - Encapsulates the logic to check whether user input into command line is correct
 
 class Compressor - Encapsulates the logic of compression or decompression of given file using class File_processor and class Huffman_coder
 
 class File_processor - Encapsulates the work with the binary files containing the compressed data
 
 class Huffman_coder - Encapsulates the Huffman coding algorithm to compress and decompress data
 
 class Node - Represents the Huffman tree to be used in the Huffman_coder
