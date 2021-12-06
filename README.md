# TKiK_Project

## Information and Entropy

This is simple python program that can be run using the command line such as:

```shell
python3 main.py <filename>
```

Program calculates entropy of a given text file as well as information of a given text file for each character. File name is required as an argument to run at least once but more filles could be passed to the program

## Huffman Compression

Implementation of huffman compression algorithm. To run the program use the command line:

```shell
python3 main.py -@param <source> <target>
```

where @param is one of the following:

- e: encode file and place it to target file
- d: decode file and place it to target file
- c: compare source and target files and print the difference

Program stores the huffman code in the target using the following format:

- 4 bytes: number of bytes in the header
- 1 byte: number of padding required
- header: describes the huffman tree structure
- file: the actual data

Program can be used to encode and decode files using utf-8 encoding as it is the most common one and it is used by default.
