#!/usr/bin/env bash

# Parse arguments
VISUAL=false
BUILD=true
PLAN=true

# Parse options
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -v|--visual )
      VISUAL=true
      ;;
    -B|--skip-build )
      BUILD=false
      ;;
    -P|--skip-plan )
      PLAN=false
      ;;
    * )
      echo "Invalid option: $1" >&2
      exit 1
      ;;
  esac
  shift
done
echo "Robot planning tester v 1.0 UwU"
cat "./test/cat.txt"
sleep 1

if [ "$BUILD" = true ]; then
  echo "Building project... (python)"
  sleep 1

  bash ./compile.sh
  echo "Compilation finished."
  sleep 1
fi


if [ "$PLAN" = true ]; then
  echo "Planning on small test case"
  sleep 1

  ./build/lifelong --inputFile ./example_problems/random.domain/random_20.json \
    --simulationTime 50 \
    --logFile ./test/log.txt \
    --output ./test/out.json\

    echo "Generated: './test/out.json'"
  sleep 1
fi
echo "Processing './test.out.json'"
python3 ./test/process.py
sleep 1

# If visual flag is set, do something
if [ "$VISUAL" = true ]; then
  echo "Starting visualisation"
  sleep 1
  python3 ../PlanViz/script/plan_viz.py \
    --map ./example_problems/random.domain/maps/random-32-32-20.map \
    --plan test/out.json \
    --grid --aid --static --ca
fi
