from .neural3d import brr
from pathlib import Path
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, type=str)
    ap.add_argument("--out-file", default="result.obj", type=Path)
    ap.add_argument("--api-link", default="https://46158.gradio.app/api/predict", type=str)
    args = ap.parse_args()
    brr(args.text, args.out_file, args.api_link)
