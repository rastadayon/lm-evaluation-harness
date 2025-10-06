import json
import re
from typing import Dict, Any, List
import math
from typing import Sequence
import numpy as np

def extract_carbs_from_answer(answer_text) -> float:
    """
    Extract numeric carbohydrate value from model output.
    - If already numeric, return as float.
    - Else, look for a JSON object and extract 'total_carbohydrates'.
    - Else, fallback to first number found in text.
    """
    if isinstance(answer_text, (int, float)):
        return float(answer_text)

    # Ensure it's a string
    answer_text = str(answer_text)

    # Try to find JSON object in the string
    match = re.search(r'\{.*?\}', answer_text)
    if match:
        try:
            obj = json.loads(match.group())
            return float(obj["total_carbohydrates"])
        except Exception:
            pass

    # Fallback: extract the first number (integer or float)
    match = re.search(r"[-+]?\d*\.\d+|\d+", answer_text)
    if not match:
        print(f'NO MATCH {"=" * 20} {answer_text}')
        return None

    return float(match.group())

def process_results(doc: Dict[str, Any], results: List[Any]) -> Dict[str, float]:
    """
    Called by LM-Eval for each document after model generation.
    - doc: processed dataset row
    - results: list of outputs for the prompt
    Returns a dict of metric -> value.
    """
    prediction_text = results[0] if results else ""
    pred_g = extract_carbs_from_answer(prediction_text)
    true_g = float(doc["carb"])

    # Compute absolute error
    if pred_g is None:
        ae = float("nan")
    else:
        ae = abs(pred_g - true_g)

    return {"mae": ae, "ae": ae}

def _finite_vals(xs: Sequence[float]) -> list[float]:
    return [x for x in xs if isinstance(x, (int, float)) and math.isfinite(x)]

def mean_ignore_nan(xs: Sequence[float]) -> float:
    vals = _finite_vals(xs)
    return float(sum(vals) / len(vals)) if vals else float("nan")

def stderr_ignore_nan(xs: Sequence[float]) -> float:
    print("HELLOOOOOO")
    vals = np.array([np.nan if v is None else v for v in xs], dtype=float)
    finite = np.isfinite(vals)
    n = int(finite.sum())
    if n <= 1:
        return float("nan") if n == 0 else 0.0
    std = np.nanstd(vals, ddof=1)  # sample stddev
    return float(std / np.sqrt(n))

def count_finite(xs: Sequence[float]) -> float:
    # handy to see how many examples actually contributed
    return float(len(_finite_vals(xs)))