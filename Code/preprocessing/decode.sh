#!/usr/bin/env bash

# $1: test name
# $2: datetime of the test
# $3: BCC file id

nome_test="$1"
bcc_id="$3"

livello_ris=2

percorso="$SCRATCH/tesi/output_$2"
nome_file_last="$nome_test-output-LAST"

frame_start=0
frame_end=$(ls $percorso/simulation* | grep -v LAST | grep ".DEP" | tail -1 | awk -F'-' '{print $NF}' | awk -F'.' '{print $1}')

swegpu=$SCRATCH/swegpu

$swegpu -decode $percorso/simulation_$bcc_id/$nome_file_last.MAXWSE $percorso/decoded_$bcc_id/$nome_test-decoded-last.MAXWSE -all -binary=0 -res=$livello_ris
$swegpu -decode $percorso/simulation_$bcc_id/$1-output-LAST.BTM $percorso/decoded_$bcc_id/$1-decoded-last.BTM -all -binary=0 -res=$livello_ris

