# Run last 5 mult scripts parallelly 
# Each mult script performs a set of 16 US trajectory simulations sequentially, all pinned to the same specific CPU
# 5 CPUs needed
for A in $(seq 41 45)
do
    bash mult/mult$A.sh &
done
