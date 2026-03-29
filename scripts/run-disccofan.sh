source vars_experiments.sh

INP_DIR=/home/mpi/host/split
HF_DIR=/home/mpi/host/hostfiles

DISCCOFAN_DIR=/home/mpi/disccofan

for i in `seq 0 $lim`
do
    
    dim=${dims[$i]}
    d1=`echo $dim | awk '{split($0,a," "); print a[1]}'`
    d2=`echo $dim | awk '{split($0,a," "); print a[2]}'`
    in_prefix_img=${INP_DIR}/dim_${d1}-${d2}-1/IMG_PHR1A__${d1}_${d2}_1
    num_proc=`expr ${d1} '*' ${d2}`
    HOSTFILE=${HF_DIR}/hosts_lins_${num_proc}proc.txt
    for ((exec=1;$exec<=$NUM_EXECS;exec+=1))
    do
        echo "grid: ${d1},${d2},1 => np: ${num_proc}, exec=${exec}"
        mpirun -np ${num_proc} --hostfile ${HOSTFILE} ${DISCCOFAN_DIR}/disccofan -g ${d1},${d2},1 --inprefix ${in_prefix_img} --intype JP2 --infile 1 --overlap 0
        sleep 10
    done
done

