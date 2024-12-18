#  https://cryptohack.org/courses/modular/root0/



from sympy import mod_inverse

# Given prime modulus
p = 29

# List of integers
ints = [14, 6, 11]

# Function to compute square modulo p
def compute_squares_modulo_p(ints, p):
    squares = [(a**2) % p for a in ints]
    return squares

# Function to compute modular inverses modulo p
def compute_modular_inverses(ints, p):
    inverses = []
    for a in ints:
        try:
            inv = mod_inverse(a, p)
            inverses.append(inv)
        except ValueError:
            inverses.append(None)  # No modular inverse if ValueError is raised
    return inverses

# Function to check quadratic residues
def check_quadratic_residues(ints, p):
    residues = []
    for a in ints:
        is_residue = False
        for x in range(p):
            if (x**2) % p == a:
                is_residue = True
                break
        residues.append(is_residue)
    return residues

# Compute squares modulo p
squares = compute_squares_modulo_p(ints, p)

# Compute modular inverses modulo p
inverses = compute_modular_inverses(ints, p)

# Check if integers are quadratic residues modulo p
residues = check_quadratic_residues(ints, p)

print(f"Squares modulo {p}: {squares}")
print(f"Modular inverses modulo {p}: {inverses}")
print(f"Quadratic residues modulo {p}: {residues}")

