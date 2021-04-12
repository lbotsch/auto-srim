#!/bin/bash

if [ "$#" -ne "2" ]; then
    echo "Usage: $0 ENERGY_FILE OUT_PATH"
    exit 1
fi

ENERGIES=()
while read -r line; do
    ENERGIES+=("$line")
done < $1
SIM_OUT_BASE=$2

echo "Simulating energies: $ENERGIES"

SIM_DIR=`readlink -f .`
ANA_DIR=`readlink -f ../..`

mkdir -p $SIM_OUT_BASE

for E in "${ENERGIES[@]}"; do
    # Delete simulation dir if it exists
    SIM_OUT_DIR="$SIM_OUT_BASE/Ar_TiO2_$E"
    if [ -f "$SIM_OUT_DIR/collisions.dat" ]; then
        echo "Collisions file for energy $E already exists! Skipping..."
        #rm -rf $SIM_OUT_DIR
    else
        echo
        echo
        echo "========================"
        echo "Energy: $E"
        echo "Start time: $(date)"
        echo "========================"
        echo
        echo

        # Do the TRIM simulation in a Docker container
        echo
        echo "========================"
        echo "Simulate energy $E eV..."
        echo "========================"
        echo
        cd $SIM_DIR
        mkdir -p $SIM_OUT_DIR
        docker run -v $PWD:/opt/pysrim/ \
               -v $SIM_OUT_DIR:/tmp/srim/SRIM\ Outputs \
               --rm \
               -it costrouc/pysrim sh -c "xvfb-run -a python3.6 /opt/pysrim/simulate.py $E"

        # Analyse the simulation results. Writes output to $SIM_OUT_DIR/dFP_per_ion.dat
        echo
        echo "========================"
        echo "Analyse energy $E eV..."
        echo "========================"
        echo
        cd $ANA_DIR
        #python count_dFP.py $SIM_OUT_DIR $NUM_UC $BINS_PER_UC
        python parse_collisions.py $SIM_OUT_DIR

        # Delete TRIM output files to save disk space (can be > 3GB)
        rm $SIM_OUT_DIR/*.txt
    fi
done
