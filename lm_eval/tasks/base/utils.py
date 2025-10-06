import re

baseline_carb_estimation_prompt = """You are a nutrition assistant that estimates carbohydrates from meal descriptions. For the given query including a meal description, respond with a dictionary object containing the total carbohydrates in grams as follows:
{"total_carbohydrates": total grams of carbohydrates for the serving}
Important:
- Only use the numeric amount of carbohydrates in the final dictionary, without extra text.
- Do **not** add extra text after the dictionary.

Follow the format of the following examples when answering-

Example 1:
Query: "This morning, I had a cup of oatmeal with half a sliced banana and a glass of orange juice."

Answer: {"total_carbohydrates": 66.5}

Example 2:
Query: "I ate scrambled eggs made with 2 eggs and a toast for breakfast."

Answer: {"total_carbohydrates": 15}

Example 3:
Query: "Half a peanut butter and jelly sandwich."

Answer: {"total_carbohydrates": 25.3}

Now answer the following query:
"""


# def doc_to_text_base(doc):
#     doc_to_text = f'{baseline_carb_estimation_prompt}\nQuery: "{doc["meal_description"]}"\nAnswer:'

#     return doc_to_text

def doc_to_text_base(doc):
    doc_to_text = f'Query: "{doc["meal_description"]}"\nAnswer:'

    return doc_to_text


def doc_to_text_cot(doc):
    doc_to_text = 'Query: "{query}"\nAnswer: Let\'s think step by step.'
    doc_to_text = doc_to_text.format(query=doc["meal_description"])

    return doc_to_text


def process_results(doc, results):
    candidates = results[0]
    pred = clean_output(candidates, doc["meal_description"], "cot", "carb")
    gt = doc["carb"]
    if pred == -1:
        mae = -1
    else:
        mae = abs(pred - gt)

    results = {
        "acc": mae < 7.5 and mae != -1,
        "mae": mae,
        "answer_rate": 1 if mae != -1 else 0,
    }
    return results


def agg_mae(items):
    items = [x for x in items if x != -1]
    mae = sum(items) / len(items)
    return mae


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def clean_output(raw_output, query, method_name, nutrition_name):

    if "cot" in method_name:
        # discard all output which is part of the reasoning process
        splits = raw_output.split("Output:")
        if len(splits) > 1: # split into reasoning and answer part
            raw_output = splits[1]
                
    raw_output = raw_output.strip()
    # print(f"Raw output: {raw_output}")
    
    # match this pattern to find the total carb estimate
    if nutrition_name == 'fat':
        pattern = r'["\']\s*total_fat["\']: (-?[0-9]+(?:\.[0-9]*)?(?:-[0-9]+(?:\.[0-9]*)?)?)'
    elif nutrition_name == 'protein':
        pattern = r'["\']\s*total_protein["\']: (-?[0-9]+(?:\.[0-9]*)?(?:-[0-9]+(?:\.[0-9]*)?)?)'
    elif nutrition_name == 'energy':
        pattern = r'["\']\s*total_energy["\']: (-?[0-9]+(?:\.[0-9]*)?(?:-[0-9]+(?:\.[0-9]*)?)?)'
    elif nutrition_name == 'carb':
        pattern = r'["\']\s*total_carbohydrates["\']:\s*(?:["\']?(-?[0-9]+(?:\.[0-9]*)?(?:-[0-9]+(?:\.[0-9]*)?)?)["\']?|\[(-?[0-9]+(?:\.[0-9]*)?(?:,\s*-?[0-9]+(?:\.[0-9]*)?)*)\])'

    else:
        raise NotImplementedError
    
    match = re.search(pattern, raw_output)
    if match:
        if match.group(1):
            pred_carbs = match.group(1) # extract the numeric part
            if is_number(pred_carbs):
                return float(pred_carbs)
            else:
                # check if output is a range
                pred_carbs_list = pred_carbs.split('-')
                if len(pred_carbs_list) == 2 and is_number(pred_carbs_list[0]) and is_number(pred_carbs_list[1]):
                    p0 = float(pred_carbs_list[0])
                    p1 = float(pred_carbs_list[1])
                    return (p0+p1)/2.0
                else:
                    print(f"EXCEPTION AFTER MATCHING")
                    print(f"Matched output: {raw_output}")
                    print(f"Query: {query}")
                    return -1
        elif match.group(2):
            try:
                pred_carbs_list = match.group(2).split(',')
                p0 = float(pred_carbs_list[0])
                p1 = float(pred_carbs_list[1])
                return (p0+p1)/2.0
            except:
                print(f"EXCEPTION AFTER MATCHING")
                print(f"Matched output: {raw_output}")
                print(f"Query: {query}")
                return -1
    else:
        if is_number(raw_output):
            return float(raw_output)
        else:
            print(f"EXCEPTION")
            print(f"Matched output: {raw_output}")
            print(f"Query: {query}")
            return -1