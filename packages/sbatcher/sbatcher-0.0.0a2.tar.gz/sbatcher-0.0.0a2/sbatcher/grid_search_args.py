import argparse
import itertools
import sys

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("nth_combination", nargs="?", type=int, default=-1)

for arg in sys.argv:
    if arg.startswith("-") and arg != "--nth-combination":
        parser.add_argument(arg, nargs="+")

args = parser.parse_args()

product = itertools.product(*(
    itertools.product([f"--{arg.replace('_', '-')}"], values)
    for arg, values in vars(args).items()
    if arg not in ("nth_combination",)
))

for n, combination in enumerate(product):
    out_args = " ".join(f"{key} {value}" for key, value in combination)
    if args.nth_combination < 0:
        print(out_args)
    elif args.nth_combination == n:
        print(out_args)

