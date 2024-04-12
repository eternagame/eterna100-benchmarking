set -e

# ===== PREP =====
mkdir -p external
pushd external
setup_root=$(pwd)

# ===== VIENNA (1.x) =====
if [ ! -d ViennaRNA-1.8.5 ]; then
    wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/1_8_x/ViennaRNA-1.8.5.tar.gz
    tar -xvf ViennaRNA-1.8.5.tar.gz
    rm ViennaRNA-1.8.5.tar.gz
fi
pushd ViennaRNA-1.8.5

./configure CFLAGS="-std=gnu89 -fcommon -g -O2" --without-perl --without-forester --without-kinfold --prefix=$setup_root/ViennaRNA-1.8.5/build
make
make check
make install

popd

# ===== VIENNA (2.1.9) =====
if [ ! -d ViennaRNA-2.1.9 ]; then
    wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_1_x/ViennaRNA-2.1.9.tar.gz
    tar -xvf ViennaRNA-2.1.9.tar.gz
    rm ViennaRNA-2.1.9.tar.gz
fi
pushd ViennaRNA-2.1.9

./configure --prefix=$setup_root/ViennaRNA-2.1.9/build --without-perl --without-forester --without-kinfold
make check
make install

popd

# ===== VIENNA (2.6.4/Current Latest) =====
if [ ! -d ViennaRNA-2.6.4 ]; then
    wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_6_x/ViennaRNA-2.6.4.tar.gz
    tar -xvf ViennaRNA-2.6.4.tar.gz
    rm ViennaRNA-2.6.4.tar.gz
fi
pushd ViennaRNA-2.6.4

./configure --prefix=$setup_root/ViennaRNA-2.6.4/build --without-perl --without-python --without-forester --without-kinfold --without-rnalocmin --without-rnaxplorer
make
make check
make install

popd

# ===== NEMO =====
if [ ! -d nemo ]; then
    git clone https://github.com/eternagame/nemo
    pushd nemo
else
    pushd nemo
    git fetch
fi
git checkout 154ada38c33efa4ccb1502f368a790d1b8124381

gcc -g -O2 -fopenmp -I../ViennaRNA-2.1.9/H -MD -MP -c -o nemo.o nemo.cpp
gcc -g -O2 -fopenmp -L../ViennaRNA-2.1.9/build/lib -o nemo nemo.o -lstdc++ -lRNA -lm -ldl

popd

# ===== ETERNABRAIN =====
if [ ! -d eternabrain ]; then
    git clone https://github.com/eternagame/eternabrain
    pushd eternabrain
else
    pushd eternabrain
    git fetch
fi
# In order to make sure our patch applies cleanly, throw out any prior modifications
# We use git stash instead of git clean just in case there were intentional local modifications
# someone wants to retrieve (the overhead incurred here should not be substantial)
git stash -u
git checkout 3b152333b579ef49ca843c497b3f11045e67b319
git apply ../eternabrain.patch

conda create -qy -p ../eternabrain-env python=2.7
# We pin grpcio to ensure it uses a prebuilt wheel
../eternabrain-env/bin/pip install -r requirements.txt grpcio==1.39.0

popd

# ===== LEARNA =====
if [ ! -d learna ]; then
    git clone https://github.com/automl/learna
    pushd learna
else
    pushd learna
    git fetch
fi
# In order to make sure our patch applies cleanly, throw out any prior modifications
# We use git stash instead of git clean just in case there were intentional local modifications
# someone wants to retrieve (the overhead incurred here should not be substantial)
git stash -u
git checkout 34b3cf9eeaab848a7fa8b1481b4abe0c416fe09e
git apply ../learna.patch

conda env create -qy -p ../learna-env --file environment.yml

popd

# ===== SENTRNA =====
if [ ! -d SentRNA ]; then
    git clone git clone https://github.com/jadeshi/SentRNA
    pushd SentRNA
else
    pushd SentRNA
    git fetch
fi
git checkout 6855a2d0734a962ffa7bf5a5833f52695644e18c

conda create -qy -p ../sentrna-env python=2.7 tensorflow=1.15.0 numpy=1.16.6

popd

popd
