from .neural3d import brr
from pathlib import Path
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, type=str)
    ap.add_argument("--out-file", default="result.obj", type=Path)
    args = ap.parse_args()
    brr(args.text, args.out_file)
