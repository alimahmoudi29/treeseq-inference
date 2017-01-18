"""
Simple CLI to run tsinf on the command line.
"""
import argparse

import numpy as np

import tsinfer

def main():

    parser = argparse.ArgumentParser(
        description="Simple CLI wrapper for tsinf")
    parser.add_argument('--verbosity', '-v', action='count', default=0)
    parser.add_argument(
        "samples",
        help="The observed haplotypes as a numpy array file")
    parser.add_argument(
        "positions",
        help="The positions of sites as a numpy array file")
    parser.add_argument(
        "output",
        help="The path to write the output file to")
    parser.add_argument(
        "-l", "--length", default=None, type=int,
        help="The total sequence length")
    parser.add_argument(
        "-r", "--recombination-rate", default=1, type=float,
        help="The scaled recombination rate.")
    parser.add_argument(
        "-t", "--threads", default=1, type=int,
        help="The number of worker threads to use")

    args = parser.parse_args()
    S = np.load(args.samples)
    pos = np.load(args.positions)
    panel = tsinf.ReferencePanel(S, pos, args.length)
    P = panel.infer_paths(args.recombination_rate, num_workers=args.threads)
    ts_new = panel.convert_records(P)
    ts_simplified = ts_new.simplify()
    ts_simplified.dump(args.output)

if __name__ == "__main__":
    main()