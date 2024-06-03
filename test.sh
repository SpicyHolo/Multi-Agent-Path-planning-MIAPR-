#!/usr/bin/env bash

echo "Robot planning tester v 1.0 UwU"
cat "./test/cat.txt"
sleep 1
echo "Building project... (python)"
sleep 1
bash ./compile.sh
echo "Compilation finished."
sleep 1
echo "Running small test case"
sleep 1
./build/lifelong --inputFile ./example_problems/random.domain/random_20.json \
    --simulationTime 50 --logFile ./test/log.txt --output ./test/out.json
echo "Produced: './test/out.json'"
sleep 1
echo "Processing file:"
python ./test/process.py
