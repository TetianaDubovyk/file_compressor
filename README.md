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
This script take input ONLY in format of a .txt file and outputs compressed data in a simple format of a .bin file

## About the algorithm
> In computer science and information theory, a Huffman code is a particular type of optimal prefix code that is commonly used for lossless data compression. The process of finding or using such a code proceeds by means of Huffman coding, an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in the 1952 paper "A Method for the Construction of Minimum-Redundancy Codes". The output from Huffman's algorithm can be viewed as a variable-length code table for encoding a source symbol (such as a character in a file). The algorithm derives this table from the estimated probability or frequency of occurrence (weight) for each possible value of the source symbol. As in other entropy encoding methods, more common symbols are generally represented using fewer bits than less common symbols. 
 
More on [Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding#Basic_technique)
 
## How does it work
### Compressor

### Decompressor

