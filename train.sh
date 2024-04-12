pushd external
EXTERNAL=$(pwd)

# Consider lowering these values if you want to generate poor models quickly just to make sure
# all the benchmarking scripts work correctly
LEARNA_TRAIN_TIMEOUT="${LEARNA_TRAIN_TIMEOUT:-3600}"
SENTRNA_TRIALS="${SENTRNA_TRIALS:-5}"
SENTRNA_MIN_FEATURES="${SENTRNA_TRIALS:-0}"
SENTRNA_MAX_FEATURES="${SENTRNA_TRIALS:-42}"

# ===== ETERNABRAIN =====
pushd eternabrain/rna-prediction

VIENNA_BIN_PATH="$EXTERNAL/ViennaRNA-1.8.5/build/bin" FEATURESET_NAME="Vienna1" "$EXTERNAL/eternabrain-env/bin/python" experts.py
VIENNA_BIN_PATH="$EXTERNAL/ViennaRNA-2.6.4/build/bin" FEATURESET_NAME="Vienna2" "$EXTERNAL/eternabrain-env/bin/python" experts.py

FEATURESET_NAME="Vienna1" TRAIN_EXTENDED_PUZZLES="false" MODEL_NAME="eterna100-benchmarking-F1-SM" "$EXTERNAL/eternabrain-env/bin/python" baseCNN.py
FEATURESET_NAME="Vienna1" TRAIN_EXTENDED_PUZZLES="false" MODEL_NAME="eterna100-benchmarking-F1-SM" "$EXTERNAL/eternabrain-env/bin/python" locationCNN.py

FEATURESET_NAME="Vienna2" TRAIN_EXTENDED_PUZZLES="false" MODEL_NAME="eterna100-benchmarking-F2-SM" "$EXTERNAL/eternabrain-env/bin/python" baseCNN.py
FEATURESET_NAME="Vienna2" TRAIN_EXTENDED_PUZZLES="false" MODEL_NAME="eterna100-benchmarking-F2-SM" "$EXTERNAL/eternabrain-env/bin/python" locationCNN.py

FEATURESET_NAME="Vienna1" TRAIN_EXTENDED_PUZZLES="true" MODEL_NAME="eterna100-benchmarking-F1-EXT" "$EXTERNAL/eternabrain-env/bin/python" baseCNN.py
FEATURESET_NAME="Vienna1" TRAIN_EXTENDED_PUZZLES="true" MODEL_NAME="eterna100-benchmarking-F1-EXT" "$EXTERNAL/eternabrain-env/bin/python" locationCNN.py

FEATURESET_NAME="Vienna2" TRAIN_EXTENDED_PUZZLES="true" MODEL_NAME="eterna100-benchmarking-F2-EXT" "$EXTERNAL/eternabrain-env/bin/python" baseCNN.py
FEATURESET_NAME="Vienna2" TRAIN_EXTENDED_PUZZLES="true" MODEL_NAME="eterna100-benchmarking-F2-EXT" "$EXTERNAL/eternabrain-env/bin/python" locationCNN.py

popd

# ===== LEARNA =====
pushd learna

./src/data/download_and_build_rfam_learn.sh
mv data/rfam_learn/test data/rfam_learn_test
mv data/rfam_learn/validation data/rfam_learn_validation
mv data/rfam_learn/train data/rfam_learn_train
rm -rf data/rfam_learn

../learna-env/bin/python -m src.learna.learn_to_design_rna \
  --data_dir data/ \
  --dataset rfam_learn_train \
  --vienna_version 1.8.5 \
  --save_path models/eterna100-benchmarking/vienna-1.8.5 \
  --timeout $LEARNA_TRAIN_TIMEOUT \
  --learning_rate 6.442010833400271e-05 \
  --mutation_threshold 5 \
  --reward_exponent 8.932893783628236 \
  --state_radius 29 \
  --conv_sizes 11 3 \
  --conv_channels 10 3 \
  --num_fc_layers 1 \
  --fc_units 52 \
  --batch_size 123 \
  --entropy_regularization 0.00015087352506343337 \
  --embedding_size 2 \
  --lstm_units 3 \
  --num_lstm_layers 0

../learna-env/bin/python -m src.learna.learn_to_design_rna \
  --data_dir data/ \
  --dataset rfam_learn_train \
  --vienna_version 2.6.4 \
  --save_path models/eterna100-benchmarking/vienna-2.6.4 \
  --timeout $LEARNA_TRAIN_TIMEOUT \
  --learning_rate 6.442010833400271e-05 \
  --mutation_threshold 5 \
  --reward_exponent 8.932893783628236 \
  --state_radius 29 \
  --conv_sizes 11 3 \
  --conv_channels 10 3 \
  --num_fc_layers 1 \
  --fc_units 52 \
  --batch_size 123 \
  --entropy_regularization 0.00015087352506343337 \
  --embedding_size 2 \
  --lstm_units 3 \
  --num_lstm_layers 0

popd

# ===== SENTRNA =====
pushd SentRNA/models

mkdir -p eterna100-benchmarking/vienna-1.8.5-rnaplot
pushd eterna100-benchmarking/vienna-1.8.5-rnaplot
for i in $(seq 1 $SENTRNA_TRIALS)
do
  for j in $(seq $SENTRNA_MIN_FEATURES $SENTRNA_MAX_FEATURES)
  do
    if [ -f 'long_range_features.pkl' ]; then
        long_range_args=( "--long_range_input" "long_range_features.pkl" )
    else
        long_range_args=()
    fi
    PATH="$PATH:$EXTERNAL/ViennaRNA-1.8.5/build/bin:./util/ViennaRNA-1.8.5/Progs/rnaplot" "$EXTERNAL/sentrna-env/bin/python" "$EXTERNAL/SentRNA/SentRNA/run.py" --mode train --input_data "$EXTERNAL/SentRNA/data/train/eterna_complete_ss.pkl" --results_path trial-${i}_MI-$j --n_long_range_features $j ${long_range_args[@]}
  done
done
popd

mkdir -p eterna100-benchmarking/vienna-2.6.4-rnaplot
pushd eterna100-benchmarking/vienna-2.6.4-rnaplot
for i in $(seq 1 $SENTRNA_TRIALS)
do
  for j in $(seq $SENTRNA_MIN_FEATURES $SENTRNA_MAX_FEATURES)
  do
    if [ -f 'long_range_features.pkl' ]; then
        long_range_args=( "--long_range_input" "long_range_features.pkl" )
    else
        long_range_args=()
    fi
    PATH="$PATH:$EXTERNAL/ViennaRNA-2.6.4/build/bin" "$EXTERNAL/sentrna-env/bin/python" "$EXTERNAL/SentRNA/SentRNA/run.py" --mode train --input_data "$EXTERNAL/SentRNA/data/train/eterna_complete_ss.pkl" --results_path trial-${i}_MI-$j --n_long_range_features $j ${long_range_args[@]}
  done
done
popd

mkdir -p eterna100-benchmarking/vienna-1.8.5-eterna
pushd eterna100-benchmarking/vienna-1.8.5-eterna
for i in $(seq 1 $SENTRNA_TRIALS)
do
  for j in $(seq $SENTRNA_MIN_FEATURES $SENTRNA_MAX_FEATURES)
  do
    if [ -f 'long_range_features.pkl' ]; then
        long_range_args=( "--long_range_input" "long_range_features.pkl" )
    else
        long_range_args=()
    fi
    PATH="$PATH:$EXTERNAL/ViennaRNA-1.8.5/build/bin:./util/ViennaRNA-1.8.5/Progs/rnaplot" "$EXTERNAL/sentrna-env/bin/python" "$EXTERNAL/SentRNA/SentRNA/run.py" --mode train --input_data "$EXTERNAL/SentRNA/data/train/eterna_complete_ss.pkl" --results_path trial-${i}_MI-$j --n_long_range_features $j --renderer eterna ${long_range_args[@]}
  done
done
popd

mkdir -p eterna100-benchmarking/vienna-2.6.4-eterna
pushd eterna100-benchmarking/vienna-2.6.4-eterna
for i in $(seq 1 $SENTRNA_TRIALS)
do
  for j in $(seq $SENTRNA_MIN_FEATURES $SENTRNA_MAX_FEATURES)
  do
    if [ -f 'long_range_features.pkl' ]; then
        long_range_args=( "--long_range_input" "long_range_features.pkl" )
    else
        long_range_args=()
    fi
    PATH="$PATH:$EXTERNAL/ViennaRNA-2.6.4/build/bin" "$EXTERNAL/sentrna-env/bin/python" "$EXTERNAL/SentRNA/SentRNA/run.py" --mode train --input_data "$EXTERNAL/SentRNA/data/train/eterna_complete_ss.pkl" --results_path trial-${i}_MI-$j --n_long_range_features $j --renderer eterna ${long_range_args[@]}
  done
done
popd

popd

popd
