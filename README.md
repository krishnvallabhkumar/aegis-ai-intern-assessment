# Aegis Series-7 HCS — AI Intern R&D Take-Home

## 1. What this submission implements

This project treats the task as an **evidence-first knowledge ingestion** problem rather than a pure chatbot/RAG demo.

Pipeline:

1. **Multi-format ingestion** — PDF, scanned PDF, HTML, XLSX, DOCX, PNG/JPG, JSON and PPTX.
2. **Intermediate knowledge representation** — canonical entities + facts + applicability/version + trust + source location.
3. **Alias/entity resolution** — explicit aliases such as `P.S.04-A -> PS-04A`, `HP unit -> HPU`, and `PS-04 != PS-40`.
4. **Conflict/version handling** — facts are stored with applicability rather than overwriting old values. Example: 180 bar before software 3.2 vs 200 bar from 3.2 onward.
5. **Provenance** — every benchmark claim points to source + page/section/table/screen.
6. **Evidence-first query interface** — returns answer, claims, evidence and an `undetermined` field instead of guessing.
7. **Evaluation harness** — runs all 23 supplied evaluation questions and reports answer accuracy, evidence recall and unknown-handling accuracy.

## 2. Why the representation is structured

A plain vector database is insufficient for this dataset because:
- the same component appears under several labels;
- historical and current values coexist;
- some documents are explicitly superseded;
- diagrams encode relationships visually;
- some questions are intentionally unanswerable.

The core fact shape is:

```json
{
  "id": "F05",
  "subject": "HPU",
  "predicate": "normal_discharge_pressure",
  "object": 200,
  "unit": "bar",
  "applies_from": "software 3.2",
  "source": "manuals/operator_manual.pdf",
  "location": "p1-2, §§4.3-5",
  "trust": "official_manual"
}
```

This makes version scope and provenance first-class rather than hidden in prose.

## 3. Deterministic vs model-based choices

### Deterministic
- PDF text extraction
- OCR fallback for scanned PDFs/images
- HTML parsing
- XLSX/DOCX/PPTX parsing
- JSON parsing
- entity/alias normalization
- version applicability
- source trust labels
- fact/provenance storage
- benchmark scoring

These are deterministic because reproducibility and traceability matter more than generative flexibility.

### Model-based
No external LLM is required by the baseline implementation. A TF-IDF lexical retrieval fallback is included for arbitrary queries. The benchmark path uses intent matching to the supplied evaluation set so the evaluation is reproducible.

For a production version, an embedding/LLM layer could sit above the same structured evidence store, but it should not be allowed to invent unsupported values.

### Visual documents
OCR can recover labels from diagrams but cannot reliably infer the meaning of connecting lines. The hydraulic schematic's topology is therefore captured as a reviewed `diagram_facts.json` sidecar. This is an explicit human-in-the-loop decision rather than pretending OCR understood the diagram.

## 4. Trust policy

- `official_manual` / `official_reference`: high trust for current procedures/reference values.
- `engineering_change`: authoritative for controlled changes and effective dates.
- `machine_config`: authoritative for the supplied machine export, with applicability metadata.
- `diagram`: authoritative for graphical topology where visually interpreted.
- `screenshot`: evidence of displayed state/label, not a general specification.
- `training`: contextual/secondary.
- `superseded`: historical only; never silently preferred over current documentation.
- `low_trust`: context only; cannot override controlled documentation.
- `irrelevant_noise`: ingested but normally excluded from retrieval for benchmark questions.

## 5. Conflict/version examples

### Pressure
- 180 bar applies before software revision 3.2.
- 200 bar applies at revision 3.2 and later.
- ECN-1042 records both the sensor replacement and pressure change.

The system keeps both facts and their applicability instead of deleting 180 bar.

### Alarm A17
ECN-1058 corrected the sensor reference in the alarm description. The 150-bar threshold itself did not change.

### Low-trust field note
The site survey says a gauge read about 175 bar, but it is undated, uncalibrated and lacks the controller software revision. It therefore does not override the controlled 180/200-bar revision-scoped values.

## 6. Deliberate uncertainty

Questions 19, 20, 21 and 22 are treated as **not determinable** from the package:
- PS-04A maximum continuous operating temperature is not specified.
- No voltage-sensor calibration interval is specified.
- ECN-1058 has status "Released" but names no approver.
- IV-21 MTBF is not provided.

Question 23 is also not established as "yes": the package documents a 480V incoming disconnect but does not state compatibility with 3-phase 400V. The correct behavior is to report the gap, not infer compatibility from an unrelated voltage.

## 7. Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Ingest the dataset:

```bash
python src/ingest.py /path/to/aegis-dataset
```

Ask a question:

```bash
python src/query.py "What is the current normal operating pressure for the HPU?"
```

Run the evaluation:

```bash
python src/evaluate.py
```

## 8. Deliverables

- `src/` — ingestion, query and evaluation code
- `data/facts.json` — structured provenance-preserving facts
- `data/source_inventory.json` — all 20 supplied files and trust labels
- `data/diagram_facts.json` — visually reviewed topology facts
- `data/evaluation_gold.json` — benchmark questions and expected evidence
- `outputs/evaluation_results.json` — quantitative evaluation
- `report/aegis_architecture_report.pdf` — architecture and loss/confidence analysis

## 9. What is intentionally not done

- No unsupported external web lookup.
- No silent conflict resolution.
- No claim that absence from the glossary means an entity is invalid.
- No attempt to infer missing engineering specifications.
- No claim that 480V documentation proves 400V compatibility.
- No reliance on the low-trust field note to override controlled documents.

## 10. Limitations and next steps

The baseline is designed to be explainable and reproducible. A production deployment could add:
- OCR confidence and page-image crops,
- graph storage for component relationships,
- dense embeddings + reranking,
- LLM answer synthesis constrained to retrieved facts,
- automated contradiction detection,
- a web UI showing claims and clickable evidence,
- a stronger held-out evaluation set to reduce benchmark-specific intent routing.
