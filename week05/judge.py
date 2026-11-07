"""Διάλεξη 10: LLM-as-judge. Ένα μοντέλο βαθμολογεί τις περιλήψεις ενός άλλου.

Χρήση:  python judge.py
"""
import json
import os
from pydantic import BaseModel, Field
from pythia_ticket import extract_ticket, strip_fences
from litellm import completion

class Score(BaseModel):
    score: int = Field(ge=1, le=5, description="1 = λάθος ή άχρηστη, 5 = ακριβής και πλήρης")
    reason: str = Field(description="Αιτιολόγηση σε μία πρόταση")

judge_model = os.getenv("MODEL_JUDGE", "anthropic/claude-haiku-5-5")
rubric = (
    "Είσαι αυστηρός αξιολογητής. Σου δίνω ένα email πελάτη και μια περίληψή του.\n"
    "Βαθμολόγησε την περίληψη από 1 έως 5:\n"
    "5: ακριβής, πλήρης, μία πρόταση\n"
    "3: σωστή αλλά λείπει κάτι σημαντικό\n"
    "1: λάθος, ή προσθέτει πράγματα που δεν λέει το email\n"
)

cases = json.load(open("eval_cases.json", encoding="utf-8"))
scores = []
for case in cases:
    text = open(case["file"], encoding="utf-8").read()
    ticket, _, _ = extract_ticket(text)
    question = rubric + "\n<email>\n" + text + "\n</email>\n\n<summary>\n" + ticket.summary + "\n</summary>"
    resp = completion(model=judge_model, messages=[{"role": "user", "content": question}], response_format=Score, num_retries=3)
    s = Score.model_validate_json(strip_fences(resp.choices[0].message.content))
    scores.append(s.score)
    print(f"{s.score}/5  {os.path.basename(case['file'])}\n     περίληψη: {ticket.summary}\n     κριτής:   {s.reason}\n")

print(f"Μέσος όρος: {sum(scores) / len(scores):.1f}/5 | κριτής: {judge_model}")
