import argparse, json, math, sys
from typing import Iterable, List, Optional
import pandas as pd
import numpy as np
import numbers
import ast

SAMPLES_FILE_PATH="/data/rasta/lm-evaluation-harness/results/nutribench_v2_baseline_llama3.1_8b/meta-llama__Meta-Llama-3.1-8B-Instruct/samples_nutribench_v2_baseline_2025-08-15T17-34-07.600724.jsonl"

def _parse_obj(x):
    """
    Try to turn a string into a Python object (JSON first, then literal_eval).
    If parsing fails, return the original value.
    """
    if isinstance(x, str):
        s = x.strip()
        # Try JSON
        try:
            return json.loads(s)
        except Exception:
            # Try Python literal (handles single quotes etc.)
            try:
                return ast.literal_eval(s)
            except Exception:
                return x
    return x

def extract_carbs_strict(val):
    """
    Extract total_carbohydrates as a float from various representations:
      - dict: {"total_carbohydrates": 12.3}
      - list of dict(s): [{"total_carbohydrates": 12.3}, ...]
      - list of stringified dict(s): ['{"total_carbohydrates": 12.3}', ...]
    Rules:
      - Only accept real numeric values (ints/floats); strings are invalid.
      - NaN/None/invalid → return None.
    """
    # NaN/None handling up front
    if pd.isna(val):
        return None

    obj = _parse_obj(val)

    candidate = None
    if isinstance(obj, dict):
        candidate = obj
    elif isinstance(obj, list):
        for item in obj:
            parsed = _parse_obj(item)
            if isinstance(parsed, dict) and "total_carbohydrates" in parsed:
                candidate = parsed
                break
    else:
        return None

    if not isinstance(candidate, dict):
        return None

    tc = candidate.get("total_carbohydrates", None)

    if isinstance(tc, numbers.Real) and not isinstance(tc, bool):
        if isinstance(tc, float) and not math.isfinite(tc):
            return None
        return float(tc)

    # Everything else (strings, None, objects) is invalid
    return None

def get_metrics_from_samples(samples_jsonl_path: str) -> None:
    """
    Load values from a JSONL file and extract specified keys.
    Returns a list of values corresponding to the keys.
    """
    df = pd.read_json(samples_jsonl_path, lines=True)
    df['pred'] = df['filtered_resps'].apply(extract_carbs_strict)
    ratio = df["pred"].notna().sum() / len(df)
    print(f"Ratio of valid predictions: {ratio:.2%}")
    
    df["ae"] = (df["pred"] - df["target"]).abs()
    mae = df["ae"].mean(skipna=True)
    std = df["ae"].std(skipna=True)
    
    print(f"MAE: {mae:.4f} ± {std:.4f}")
    

def main():
    ap = argparse.ArgumentParser(description="Summarize LM-Eval samples.jsonl (MAE/STD/SEM & counts).")
    ap.add_argument("samples_jsonl", help="Path to samples.jsonl", default=SAMPLES_FILE_PATH)

    ap.add_argument(
        "--out",
        default=None,
        help="Optional path to write a tiny JSON summary (prints to stdout regardless).",
    )
    args = ap.parse_args()

    get_metrics_from_samples(args.samples_jsonl)