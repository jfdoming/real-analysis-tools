from atools import *

def print_info(set_to_analyze, name):
    print(f"{name} = {set_to_analyze}")
    print(f"closure({name}) = {set_to_analyze.cl()}")
    print(f"closure({name}^c) = {set_to_analyze.co().cl()}")
    print(f"int({name}) = {set_to_analyze.it()}")
    print(f"int({name}^c) = {set_to_analyze.co().it()}")

    print("-------------------")
    print(f"number of sets under closure and complement = {count(set_to_analyze)}")

    print(f"sets under closure and complement = {compute(set_to_analyze)}")
    print("-------------------")

# You can define sets like this:
A = (Q * C(0, 1)) + U(2,3) + U(3,4) + N(4)
print_info(A, "A")

# Or like this:
B = SM(RU(0, 1), N(0))
print_info(B, "B")

# Your sets will be simplified where possible.
C = X - (X - Q)
print(f"C = X - (X - Q) was simplified to {C}")

D = U(0, 1) + U(1, 2) + U(2, 3)
E = F(0, 1, 2)
print(f"D = {D}")
print(f"E = {E}")
print(f"D + E = {D + E}")
print("-------------------")

# You can also export sets to LaTeX!
print(to_latex(A))

for S in compute(A):
    print(to_latex(S, inline=False))