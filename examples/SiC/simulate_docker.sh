
if [ "$#" -ne "1" ]; then
    echo "Usage: $0 ENERGY"
    exit 1
fi

docker run -v $PWD:/opt/pysrim/ \
       -v $PWD/output:/tmp/srim_output \
       -v $PWD/tmp:/tmp/srim/SRIM\ Outputs \
       --rm \
       -it costrouc/pysrim sh -c "xvfb-run -a python3.6 /opt/pysrim/simulate.py $1"
