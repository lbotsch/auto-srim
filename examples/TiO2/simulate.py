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

TiO2_layer = Layer({
    "Ti": {
        "stoich": 1.0,
        "E_d": 39.0,
        "lattice": 0.0,
        "surface": 3.0,
    },
    "O": {
        "stoich": 2.0,
        "E_d": 19.0,
        "lattice": 0.0,
        "surface": 3.0
    }
}, density=4.23, width=100000.0)
TiO2_target = Target([TiO2_layer])

try:
    print("Simulating Ar (%d eV) -> TiO2 [%d Ions]" % (energy, NIONS))
    Ar_ion = Ion("Ar", energy=energy)

    trim = TRIM(TiO2_target, Ar_ion, **TRIM_PARAMS)
    results = trim.run("/tmp/srim")

except Exception as e:
    print("Analysis failed!")
finally:
    # Copy output files
    #out_dir = "/tmp/srim_output/last"
    #os.makedirs(out_dir, exist_ok=True)
    #TRIM.copy_output_files("/tmp/srim", out_dir)
    pass
