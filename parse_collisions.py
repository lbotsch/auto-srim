import os, sys
import srim

if len(sys.argv) <= 1:
    print("Usage: python %s PATH" % __file__)
    exit(1)

ATOMS = {i+1:symb for i,symb in enumerate(["H", "He",
                                           "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne",
                                           "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar",
                                           "K",  "Ca", "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "As", "Se", "Br", "Kr",
                                           "Rb", "Sr", "Y",  "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I",  "Xe",
                                           "Cs", "Ba", "La", "Ce", "Pr", "Ne", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po"])}


DATA_PATH = sys.argv[1]

DEBUG = False



def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)



print("Processing file '%s'" % DATA_PATH)
coll = srim.output.Collision(DATA_PATH)

collisions = {}

num_ions = len(coll)
with open(os.path.join(DATA_PATH, "collisions.dat"), "w") as outfile:
    outfile.write("# Nions = %d\n" % num_ions)
    outfile.write("Atom,Depth (nm),Energy (eV),Primary\n")
    for ion_idx in range(num_ions):
        try:
            ion = coll[ion_idx]
            if len(ion["collisions"]) > 0:
                for c in ion["collisions"]:
                    if c["cascade"] is not None:
                        for rec in c["cascade"]:
                            atom = ATOMS[rec["atom"]]
                            depth = rec["position"][0]/10.0
                            energy = rec["recoil_energy"]
                            primary = 1 if rec["prim"] else 0
                            outfile.write("%s,%.8g,%.8g,%d\n" % (atom, depth, energy, primary))
            sys.stderr.write("Ion %d/%d (%.02f %%)                      \r" % (ion_idx+1, num_ions, (ion_idx+1)/num_ions*100))
        except Exception as e:
            print("Ion %d failed: %s" % (ion_idx+1, repr(e)))
            raise

    sys.stderr.write("                                             \n")
