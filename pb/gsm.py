import json
import re
import os

def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]
    
def get_examples(split):
    path = os.path.join("data/", f"{split}.jsonl")
    examples = read_jsonl(path)

    for ex in examples:
        ex.update(question=ex["question"] + "\n")
        ex.update(answer=ex["answer"] + "<|endoftext|>")

    print(f"{len(examples)} {split} examples")
    return examples


ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
INVALID_ANS = "[invalid]"


def gsm_extract_answer(completion):
    match = ANS_RE.search(completion)
    if match:
        match_str = match.group(1).strip()
        match_str = match_str.replace(",", "")
        return match_str
    else:
        return INVALID_ANS
    
def gsm_is_correct(model_completion, gt_example):
    gt_answer = gsm_extract_answer(gt_example["answer"])
    assert gt_answer != INVALID_ANS
    return gsm_extract_answer(model_completion) == gt_answer

def gsm_extract_selected(ans):
    if len(ans) == 1:
        return [ans]
    pattern = "(^|\s)[ABCD](, [ABCD])*($|\s)"
    a = re.search(pattern, ans)
    if a:
        text = ans[a.start():a.end()]
        predictions = text.replace(" ", "").split(",")
        
    else:
        predictions = []
        for answer_opt in "ABCD":
            pattern = "{}: ".format(answer_opt)
            a = re.search(pattern,ans)
            if a:
                predictions += answer_opt
    return predictions

def gsm_is_options(model_completion, gt_example):
    gt_answer = gsm(gt_example["answer"])
    return gsm_extract_selected(model_completion) == gt_answer