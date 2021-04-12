# Auto-SRIM - Automation of SRIM collision cascade simulations

## Prerequisits

 - Python (>= 3.6)
 - pyyaml, numpy (>= 1.10.0)
 - Docker (>= 19.03.12): https://docs.docker.com/engine/install/

## Usage

Example usage of this package can be found in the `examples` directory. To run the examples,
use the following commands:

```bash
cd examples/TiO2
./sim_and_analyze.sh energies.txt $(pwd)/Ar
```

This will run collision cascade simulations of Ar ions into TiO2 at the ion
energies listed in the file `energies.txt` and put the results into the
directory `Ar`.
