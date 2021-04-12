import os, sys
from srim import TRIM, Ion, Layer, Target
from srim.output import Results

if len(sys.argv) <= 1:
    print("Usage: python %s ENERGY" % __file__)
    exit(1)

energy = float(sys.argv[1])

NIONS = 10000

TRIM_PARAMS = dict(
    calculation = 2,
    number_ions = NIONS,
    collisions = 2,
    sputtered = 1,
)

SiC_layer = Layer({
    "Si": {
        "stoich": 1.0,
        "E_d": 40.0,
        "lattice": 0.0,
        "surface": 3.0,
    },
    "C": {
        "stoich": 1.0,
        "E_d": 25.0,
        "lattice": 0.0,
        "surface": 3.0
    }
}, density=3.21, width=100000.0)
SiC_target = Target([SiC_layer])

try:
    print("Simulating Ar (%d eV) -> SiC [%d Ions]" % (energy, NIONS))
    Ar_ion = Ion("Ar", energy=energy)

    trim = TRIM(SiC_target, Ar_ion, **TRIM_PARAMS)
    results = trim.run("/tmp/srim")

except Exception as e:
    print(e)
    print("Analysis failed!")
finally:
    # Copy output files
    #out_dir = "/tmp/srim_output/last"
    #os.makedirs(out_dir, exist_ok=True)
    #TRIM.copy_output_files("/tmp/srim", out_dir)
    pass
