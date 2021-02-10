#!/usr/bin/env bash

export test_name="input_toce_ris_V17_50.txt"
export date=$(date '+%d-%m-%Y_%H.%M')

for bcc in ./input/BCC/*; do
    export bcc_id=$(echo $bcc | awk -F'.' '{print $2}' | tail -c 4)
    export bcc=$(basename $bcc)

    mkdir -p $SCRATCH/tesi/output_$date/{simulation_$bcc_id,decoded_$bcc_id}

    sbatch simulation.slurm
    echo "bcc number: $bcc_id"
done

