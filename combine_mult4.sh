# Run fourth 10 mult scripts parallelly 
# Each mult script performs a set of 16 US trajectory simulations sequentially, all pinned to the same specific CPU
# 10 CPUs needed
for A in $(seq 31 40)
do
    bash mult/mult$A.sh &
done
