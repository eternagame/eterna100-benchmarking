# ===== PREP =====
mkdir -p external
pushd external
setup_root=$(pwd)

# ===== VIENNA (1.x) =====
wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/1_8_x/ViennaRNA-1.8.5.tar.gz
tar -xvf ViennaRNA-1.8.5.tar.gz
rm ViennaRNA-1.8.5.tar.gz
pushd ViennaRNA-1.8.5

./configure CFLAGS="-std=gnu89 -fcommon -g -O2" --without-perl --without-forester --without-kinfold --prefix=$setup_root/ViennaRNA-1.8.5/build
make
make check
make install

popd

# ===== VIENNA (2.1.9) =====
wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_1_x/ViennaRNA-2.1.9.tar.gz
tar -xvf ViennaRNA-2.1.9.tar.gz
rm ViennaRNA-2.1.9.tar.gz
pushd ViennaRNA-2.1.9

./configure --prefix=$setup_root/ViennaRNA-2.1.9/build --without-perl --without-forester --without-kinfold
make check
make install

popd

# ===== VIENNA (2.6.4/Current Latest) =====
wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_6_x/ViennaRNA-2.6.4.tar.gz
tar -xvf ViennaRNA-2.6.4.tar.gz
rm ViennaRNA-2.6.4.tar.gz
pushd ViennaRNA-2.6.4

./configure --prefix=$setup_root/ViennaRNA-2.6.4/build --without-perl --without-python --without-forester --without-kinfold --without-rnalocmin --without-rnaxplorer
make
make check
make install

popd

# ===== NEMO =====
git clone https://github.com/eternagame/nemo
pushd nemo
git checkout 154ada38c33efa4ccb1502f368a790d1b8124381

gcc -g -O2 -fopenmp -I../ViennaRNA-2.1.9/H -MD -MP -c -o nemo.o nemo.cpp
gcc -g -O2 -fopenmp -L../ViennaRNA-2.1.9/build/lib -o nemo nemo.o -lstdc++ -lRNA -lm -ldl

popd

# ===== ETERNABRAIN =====
git clone https://github.com/eternagame/eternabrain
pushd eternabrain
git checkout 3b152333b579ef49ca843c497b3f11045e67b319
git apply ../eternabrain.patch

conda create -qy -p ../eternabrain-env python=2.7
# We pin grpcio to ensure it uses a prebuilt wheel
../eternabrain-env/bin/pip install -r requirements.txt grpcio==1.39.0

popd

# ===== LEARNA =====
git clone https://github.com/automl/learna
pushd learna
git checkout 34b3cf9eeaab848a7fa8b1481b4abe0c416fe09e
git apply ../learna.patch

conda env create -qy -p ../learna-env --file environment.yml

# ===== SENTRNA =====
git clone https://github.com/jadeshi/SentRNA
pushd SentRNA
git checkout 6855a2d0734a962ffa7bf5a5833f52695644e18c

conda create -qy -p ../sentrna-env python=2.7 tensorflow=1.15.0 numpy=1.16.6
