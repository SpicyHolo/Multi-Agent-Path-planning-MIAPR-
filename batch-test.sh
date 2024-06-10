warehouse_small_sizes=(10 50 60 100 200 400 800)
# Set the map_name variable
map_name="warehouse_small"

# Iterate over the range 0 to 5
for map_size in {0..6}; do
    # Get the corresponding value from the array
    size=${warehouse_small_sizes[$map_size]}
    

    
    # Run the command
    ./test.sh -B --map $map_name --size $map_size
    
    # Copy the contents of the test folder to the new directory
    sleep 5
    mv "./test/out.json" "./tests/${map_name}_${size}_spacetime.json"
done

