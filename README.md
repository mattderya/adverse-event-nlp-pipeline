# 🧬 Adverse Event NLP Pipeline
### Clinical Insights Extraction from Pharmaceutical Literature

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange.svg)](https://huggingface.co)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00.svg)](https://tensorflow.org)
[![Kaggle](https://img.shields.io/badge/Kaggle-Notebook-20BEFF.svg)](https://kaggle.com/mderya)

---

## 🎯 Project Overview

During my work at **Mentor R&D**, I developed NLP pipelines to automatically extract clinical insights from **scientific literature and adverse event reports** — a critical capability for Oncology and Immunology drug development programs.

Manual review of thousands of PubMed abstracts was taking weeks and introducing human error into pharmacovigilance workflows.

**This repository demonstrates the core methodology using publicly available data.**

---

## ⚠️ Replica Notice

> The original pipeline processed **proprietary adverse event reports** and internal clinical documents protected under **HIPAA compliance**. This repo uses the **PubMed 200k RCT** dataset as a publicly available proxy with identical methodology.

| | This Repo | Production Pipeline |
|---|---|---|
| **Dataset** | Public PubMed 200k RCT | Proprietary adverse event reports |
| **Model** | DistilBERT | BioBERT fine-tuned |
| **Scale** | ~50k samples | Millions of documents |

---

## 📊 Production Results (Mentor R&D)

- ⚡ Abstract screening time reduced from **weeks → hours**
- 🎯 Enabled faster adverse event signal detection for **Oncology/Immunology** programs
- 📊 Processed **millions of sentences** from PubMed and internal reports
- 🏥 Full **HIPAA compliance** maintained throughout

---

## 🛠️ Te
