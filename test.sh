#!/usr/bin/env bash

# Parse arguments
VISUAL=false
BUILD=true
PLAN=true

MAP="random"
SIZE=0

MAP_PATH="./example_problems/"
PROBLEM_PATH="./example_problems/"

# Arrays for map sizes
warehouse_small_sizes=(10 50 60 100 200 400 800)
warehouse_large_sizes=(200 400 600 800 1000 2000 3000 4000 5000 8000)
random_sizes=(20 50 100 200 400 600 800)
city_sizes=(200 300 400 500 1000 2000 3000 5000 8000)
game_sizes=(200 300 400 500 1000 2000 3000 5000 8000)
sortation_large_sizes=(400 600 800 1200 1600 2000 2400 3000 5000 8000)

# Function to print usage
print_usage() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -v, --visual               Enable visual mode"
  echo "  -B, --skip-build           Skip the build process"
  echo "  -P, --skip-plan            Skip the planning step"
  echo "  --map MAP                  Choose map (warehouse_small, warehouse_large, random, city, game, sortation_large)"
  echo "  --size SIZE                Index in array of sizes for the chosen map"
  echo "maps=(warehouse_small warehouse_large random city game sortation_large)"
  echo "warehouse_small_sizes=(10 50 60 100 200 400 800)"
  echo "warehouse_large_sizes=(200 400 600 800 1000 2000 3000 4000 5000 8000)"
  echo "random_sizes=(20 50 100 200 400 600 800)"
  echo "city_sizes=(200 300 400 500 1000 2000 3000 5000 8000)"
  echo "game_sizes=(200 300 400 500 1000 2000 3000 5000 8000)"
  echo "sortation_large_sizes=(400 600 800 1200 1600 2000 2400 3000 5000 8000)"
}

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
    --map )
      MAP="$2"
      shift
      ;;
    --size )
      SIZE="$2"
      shift
      ;;
    -h|--help )
      print_usage
      exit 0
      ;;
    -* )
      # Process combined short options
      for (( i=1; i<${#1}; i++ )); do
        case "${1:i:1}" in
          v )
            VISUAL=true
            ;;
          B )
            BUILD=false
            ;;
          P )
            PLAN=false
            ;;
          * )
            echo "Invalid option: -${1:i:1}" >&2
            print_usage
            exit 1
            ;;
        esac
      done
      ;;
    * )
      echo "Invalid option: $1" >&2
      print_usage
      exit 1
      ;;
  esac
  shift
done

# Validate map and size
case "$MAP" in
  warehouse_small)
    VALID_SIZES=("${warehouse_small_sizes[@]}")
    MAP_PATH+="warehouse.domain/maps/warehouse_small.map"
    PROBLEM_PATH+="warehouse.domain/warehouse_small_"
    ;;
  warehouse_large)
    VALID_SIZES=("${warehouse_large_sizes[@]}")
    MAP_PATH+="warehouse.domain/maps/warehouse_large.map"
    PROBLEM_PATH+="warehouse.domain/warehouse_large_"
    ;;
  random)
    VALID_SIZES=("${random_sizes[@]}")
    MAP_PATH+="random.domain/maps/random-32-32-20.map"
    PROBLEM_PATH+="random.domain/random_"
    ;;
  city)
    VALID_SIZES=("${city_sizes[@]}")
    MAP_PATH+="city.domain/maps/Paris_1_256.map"
    PROBLEM_PATH+="city.domain/paris_"
    ;;
  game)
    VALID_SIZES=("${game_sizes[@]}")
    MAP_PATH+="game.domain/maps/brc202d.map"
    PROBLEM_PATH+="game.domain/brc202d_"
    ;;
  sortation_large)
    VALID_SIZES=("${sortation_large_sizes[@]}")
    MAP_PATH+="warehouse.domain/sortation_large.map"
    PROBLEM_PATH+="warehouse.domain/sortation_large_"
    ;;
  *)
    echo "Invalid map: $MAP" >&2
    print_usage
    exit 1
    ;;
esac

if ! [[ "$SIZE" =~ ^[0-9]+$ ]] || [ "$SIZE" -lt 0 ] || [ "$SIZE" -ge "${#VALID_SIZES[@]}" ]; then
  echo "Invalid size index for map $MAP. Must be between 0 and $((${#VALID_SIZES[@]} - 1))." >&2
  print_usage
  exit 1
fi

# Get the actual size value
ACTUAL_SIZE=${VALID_SIZES[$SIZE]}
PROBLEM_PATH+="${ACTUAL_SIZE}.json"

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

  ./build/lifelong --inputFile "$PROBLEM_PATH" \
    --simulationTime 200 \
    --logFile ./test/log.txt \
    --output ./test/out.json

  echo "Generated: './test/out.json'"
  sleep 1
fi

echo "Processing './test/out.json'"
python3 ./test/process.py
sleep 1

# If visual flag is set, do something
if [ "$VISUAL" = true ]; then
  echo "Starting visualisation"
  sleep 1
  python3 ../PlanViz/script/plan_viz.py \
    --map "$MAP_PATH" \
    --plan ./test/out.json \
    --grid --aid --static --ca
fi

