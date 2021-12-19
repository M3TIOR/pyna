# BioEncoding bytecode

## Encoded File Signature

| # | Bytecode      |            Description              |
|:-:|:-------------:|:------------------------------------|
| 0 | ```0xEA```    | Unique File Type Identifier
| 1 | ```0x42```    | B "ASCII"
| 2 | ```0x49```    | I "ASCII"
| 3 | ```0x4f```    | O "ASCII"
| 4 | ```0x0d```    | ASCII Bell Return
| 5 | ```0x0a```    | ASCII New Line
| 6 | ```0x1a```    | CTRL-Z - stops display under ms-dos
| 7 | ```0x0a```    | ASCII New Line

Largely inspired by the PNG file signature, this signature both identifies the file as a BioEncoded file and provides for immediate detection of common file-transfer problems. The first two bytes distinguish BioEncoded files on systems that expect the first two bytes to identify the file type uniquely. The first byte is chosen as a non-ASCII value to reduce the probability that a text file may be misrecognized as a BioEncoded file; also, it catches bad file transfers that clear bit 7. Bytes two through four name the format. The CR-LF sequence catches bad file transfers that alter newline sequences. The control-Z character stops file display under MS-DOS. The final line feed checks for the inverse of the CR-LF translation problem.

## Encoding Metadata

The encoding metadata immediately succeeds the signature, and contains the information necessary to decode the binary into its text form.

|  Byte Index  |      Description      |
|:------------:|:----------------------|
|     1-3      | Zero value nucleotide pair
|     4-6      | One value nucleotide pair
|     7-9      | Two value nucleotide pair
|    10-12     | Three value nucleotide pair

#### Nucleotide Pairs
Each nucleotide pair is identified as a three byte segment. The first byte in each nucleotide pair is the character identifier respective to the value of the current identifier index starting with zero. The second byte is the current nucleotide's sibling. Finally, each nucleotide is terminated by a newline character.

## Chunk Data

Each segment of binary data is held in a chunk. Each of these chunks holds from one to 251 bytes of data following the nucleotide count. The Nucleotide count is the number of nucleotides in the chunk. To get the bytes of data contained in the chunk, divide the nucleotide count by four.

|  Byte Index   |      Description      |
|:-------------:|:----------------------|
|     0-3       | Nucleotide Count
|     4+N       | Data
