# raven_magnet

Sample code for publishing [Magnet links](https://en.wikipedia.org/wiki/Magnet_URI_scheme) (commonly used in peer to peer file sharing) in the [Ravencoin](https://ravencoin.org/) blockchain

The code uses Raven asset names to store metadata (e.g. a filename or keywords) that can be searched for using the Ravencoin client or blockchain explorer websites

The hash of the file is stored in the txid_hash field of the RVN asset. 
Originally intended to store Open Index Protocol txid hashes, this field can in fact be used to store any data within the 32 byte limit

Therefore this also serves as an example of storing indexable, generic data within the Ravencoin blockchain

### Requirements

Python 3.5+  
python-ravencoinlib (`pip3 install python-ravencoinlib`)

### Usage
#### Publish to network:
`issue-link.py TEST 'magnet:?xt=urn:btih:fef0b1b70717c8376f5c7fac90f6e71acdb00c5b&dn=tails-amd64-4.3-img`  

Result: RVN txid if successful  

TEST is any RVN asset name owned by your wallet. Recommended to use a 3 or 4 character asset name as this allows maximum space for the keywords/filename.  
Filename will be automatically extracted from the 'dn=' section of the magnet link. However, this may result in an asset name which is too long. In this case, you can specify a name of your own using `--filename`.

#### Recover from network:
`recover-links.py TEST`

#### Decode a link manually
`decode.py 'TEST#tails-amd64-4.3-img' '4d41474e0014fef0b1b70717c8376f5c7fac90f6e71acdb00c5b000000000000'`  

Result: magnet:?xt=urn:btih:fef0b1b70717c8376f5c7fac90f6e71acdb00c5b&dn=tails-amd64-4.3-img

### Technical details
Metadata is stored as a Ravencoin unique asset of the form BASE#METADATA  
Where BASE is any asset name owned by the issuer  
#METADATA can be a filename or keywords intended to be searchable by other users

The total length of the BASE#METADATA string is limited to 31 characters

The magnet hash is stored as binary data in the txid_hash field with the following format:  
* 4 bytes identifier 'MAGN'
* 1 byte unsigned char: hash type (e.g. btih, sha1 - see source for list)
* 1 byte unsigned char: length of hash bytes
* up to 26 bytes - hash bytes (zero padded up to 32 bytes total)

