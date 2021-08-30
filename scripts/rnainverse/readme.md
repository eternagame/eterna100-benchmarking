`performance1.py` runs RNAinverse on Vienna 1

`performance2.py` runs RNAinverse on Vienna 2

To install Vienna 1.8.5:
- [Download](https://www.tbi.univie.ac.at/RNA/#old) Vienna 1.8.5, and unpack with `tar -zxvf ViennaRNA-1.8.5.tar.gz`
- On lines 826 and 896 of lib/fold.c, delete INLINE on HairpinE and LoopEnergy methods
- Run ./configure, make, make install

