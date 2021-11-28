# Python text files compressor based on Huffman's compression algorithm
#### Video Demo:  <URL HERE>
## Table of Contents

* [How to use it](#how-to-use-it)
* [Input and output formats](#input-and-output-formats)
* [About the algorithm](#about-the-algorithm)
* [How does it work](#how-does-it-work)
  * [Compressor](#compressor)
  * [Decompressor](#decompressor)

## How to use it
The script requires the following parameters to be launched: 

 to compress a file:
 ```
 python text_file_copmressor.py compress FILE.txt FILE.bin
```
to decompress a file:
 ```
 python text_file_copmressor.py decompress FILE.bin FILE.txt
```
## Input and output formats
For compression this script takes input ONLY in format of .txt file and outputs compressed data in a simple format of .bin file
For decompression it takes input ONLY in format of .bin file and outputs compressed data in a format of .txt file

## About the algorithm
> Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.
The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream.  
 
More about Huffman coding on [Wikipedia, Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding#Basic_technique)
 
## How does it work
### Compressor

### Decompressor

