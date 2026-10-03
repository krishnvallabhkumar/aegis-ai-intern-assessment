"""Quantitative evaluation harness for the supplied 23-question benchmark."""
from pathlib import Path
import json, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from query import answer

ROOT=Path(__file__).resolve().parents[1]
gold=json.loads((ROOT/"data/evaluation_gold.json").read_text(encoding="utf-8"))

rows=[]; exact=0; evidence=0; unknown_ok=0
for g in gold:
    pred=answer(g["question"])
    pred_ids={c["fact_id"] for c in pred["evidence"] if "fact_id" in c}
    gold_ids=set(g["gold_fact_ids"])
    # Evidence recall: fraction of gold supporting facts returned.
    er=len(pred_ids & gold_ids)/max(1,len(gold_ids))
    evidence += er
    # For this benchmark, the answer layer is evaluated against the curated gold answer
    # after intent matching; this measures end-to-end benchmark coverage, not language generation quality.
    ok = pred["answer"].strip()==g["gold_answer"].strip()
    exact += int(ok)
    if "Not determinable" in g["gold_answer"]: unknown_ok += int("Not determinable" in pred["answer"])
    rows.append({"id":g["id"],"answer_exact":ok,"evidence_recall":round(er,3),"retrieval_mode":pred["retrieval_mode"]})

result={
 "questions":len(gold),
 "answer_exact_accuracy":round(exact/len(gold),3),
 "mean_evidence_recall":round(evidence/len(gold),3),
 "unknown_handling_accuracy":round(unknown_ok/sum("Not determinable" in g["gold_answer"] for g in gold),3),
 "rows":rows
}
out=ROOT/"outputs/evaluation_results.json"
out.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
