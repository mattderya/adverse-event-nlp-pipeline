import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Adverse Event NLP Pipeline",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Adverse Event NLP Pipeline")
st.caption("Clinical Insights Extraction from Pharmaceutical Literature | Built by [Matt Derya](https://mattderya.com)")

st.info(
    "**Demo Notice:** This app demonstrates the NLP pipeline architecture using mock data. "
    "The production system at Mentor R&D processes proprietary adverse event reports under HIPAA compliance."
)

with st.sidebar:
    st.header("⚙️ Model Settings")
    model_choice = st.selectbox("NLP Model", ["DistilBERT", "BioBERT", "SciBERT"])
    task = st.selectbox("Task", [
        "Sentence Classification",
        "Adverse Event Extraction",
        "Named Entity Recognition",
        "Sentiment Analysis"
    ])
    st.divider()
    st.markdown("### 📋 Example Texts")
    examples = [
        "Patient experienced severe nausea and vomiting after administration of MRD-112.",
        "No significant adverse events were reported during the 12-week treatment period.",
        "The drug demonstrated significant tumor reduction in Phase II Oncology trial.",
        "Elevated liver enzymes (ALT 3x ULN) observed in 12% of patients.",
        "Treatment discontinued due to grade 3 peripheral neuropathy.",
    ]
    for ex in examples:
        if st.button(ex[:50] + "...", use_container_width=True):
            st.session_state["prefill"] = ex
    st.divider()
    st.markdown("**Tech Stack**")
    st.markdown("DistilBERT · BioBERT · HuggingFace · TensorFlow")

ADVERSE_KEYWORDS = {
    "severe": "HIGH", "nausea": "MODERATE", "vomiting": "MODERATE",
    "discontinued": "HIGH", "toxicity": "HIGH", "elevated": "MODERATE",
    "neuropathy": "HIGH", "hepatotoxicity": "HIGH", "fatigue": "LOW",
    "headache": "LOW", "rash": "MODERATE", "grade 3": "HIGH", "grade 4": "HIGH",
    "ULN": "MODERATE", "adverse": "MODERATE", "side effect": "MODERATE"
}

SENTENCE_LABELS = {
    "background": ("🔵", "Background"),
    "objective": ("🟣", "Objective"),
    "methods": ("🟡", "Methods"),
    "results": ("🟢", "Results"),
    "conclusions": ("🟠", "Conclusions"),
}

def classify_sentence(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["background", "introduction", "previously"]):
        return "background"
    elif any(w in text_lower for w in ["objective", "aim", "purpose", "we sought"]):
        return "objective"
    elif any(w in text_lower for w in ["method", "patient", "administered", "treatment", "dose"]):
        return "methods"
    elif any(w in text_lower for w in ["result", "observed", "found", "demonstrated", "showed", "reported"]):
        return "results"
    elif any(w in text_lower for w in ["conclusion", "therefore", "thus", "suggest", "indicate"]):
        return "conclusions"
    else:
        return "results"

def extract_adverse_events(text):
    events = []
    for keyword, severity in ADVERSE_KEYWORDS.items():
        if keyword.lower() in text.lower():
            events.append({"term": keyword, "severity": severity})
    return events

def extract_entities(text):
    entities = []
    drug_patterns = ["MRD-", "warfarin", "amiodarone", "metformin", "simvastatin"]
    for drug in drug_patterns:
        if drug.lower() in text.lower():
            entities.append({"entity": drug, "type": "DRUG", "color": "blue"})
    if any(w in text.lower() for w in ["patient", "subjects", "participants"]):
        entities.append({"entity": "Patient population", "type": "POPULATION", "color": "green"})
    if any(w in text.lower() for w in ["phase ii", "phase iii", "trial", "study"]):
        entities.append({"entity": "Clinical trial", "type": "STUDY_TYPE", "color": "purple"})
    numbers = re.findall(r'\d+(?:\.\d+)?%', text)
    for n in numbers:
        entities.append({"entity": n, "type": "PERCENTAGE", "color": "orange"})
    return entities

def analyze_text(text, task, model):
    results = {"task": task, "model": model, "text": text}
    if task == "Sentence Classification":
        label = classify_sentence(text)
        icon, label_name = SENTENCE_LABELS.get(label, ("⚪", "Unknown"))
        results["label"] = label_name
        results["icon"] = icon
        results["confidence"] = 0.87 if model == "BioBERT" else 0.82
    elif task == "Adverse Event Extraction":
        results["events"] = extract_adverse_events(text)
    elif task == "Named Entity Recognition":
        results["entities"] = extract_entities(text)
    elif task == "Sentiment Analysis":
        text_lower = text.lower()
        if any(w in text_lower for w in ["severe", "discontinued", "toxicity", "grade 3", "grade 4"]):
            results["sentiment"] = "Negative"
            results["score"] = 0.91
        elif any(w in text_lower for w in ["no significant", "well tolerated", "safe", "effective"]):
            results["sentiment"] = "Positive"
            results["score"] = 0.88
        else:
            results["sentiment"] = "Neutral"
            results["score"] = 0.75
    return results

if "prefill" in st.session_state:
    default_text = st.session_state.pop("prefill")
else:
    default_text = "Patient experienced severe nausea and vomiting after administration of MRD-112."

text_input = st.text_area(
    "Enter clinical text to analyze:",
    value=default_text,
    height=120,
    placeholder="Enter pharmaceutical literature text, adverse event report, or clinical trial abstract..."
)

col_btn, col_batch = st.columns([1, 3])
analyze_btn = col_btn.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze_btn and text_input:
    result = analyze_text(text_input, task, model_choice)

    st.divider()
    st.markdown(f"### Results — {task} ({model_choice})")

    if task == "Sentence Classification":
        col1, col2 = st.columns(2)
        col1.metric("Classification", f"{result['icon']} {result['label']}")
        col2.metric("Confidence", f"{result['confidence']:.0%}")
        st.markdown(f"**Sentence type:** The model classified this as a **{result['label']}** sentence from a clinical abstract.")

    elif task == "Adverse Event Extraction":
        events = result["events"]
        if events:
            severity_colors = {"HIGH": "🔴", "MODERATE": "🟡", "LOW": "🟢"}
            df = pd.DataFrame(events)
            df["severity_icon"] = df["severity"].map(severity_colors)
            df["display"] = df["severity_icon"] + " " + df["term"] + " (" + df["severity"] + ")"
            st.markdown("**Detected adverse event signals:**")
            for _, row in df.iterrows():
                st.markdown(f"- {row['display']}")
            high = len(df[df["severity"] == "HIGH"])
            mod = len(df[df["severity"] == "MODERATE"])
            low = len(df[df["severity"] == "LOW"])
            c1, c2, c3 = st.columns(3)
            c1.metric("High severity", high)
            c2.metric("Moderate", mod)
            c3.metric("Low", low)
        else:
            st.success("✅ No adverse event signals detected.")

    elif task == "Named Entity Recognition":
        entities = result["entities"]
        if entities:
            st.markdown("**Extracted entities:**")
            type_colors = {"DRUG": "🔵", "POPULATION": "🟢", "STUDY_TYPE": "🟣", "PERCENTAGE": "🟠"}
            for ent in entities:
                icon = type_colors.get(ent["type"], "⚪")
                st.markdown(f"- {icon} **{ent['entity']}** — `{ent['type']}`")
        else:
            st.warning("No named entities detected.")

    elif task == "Sentiment Analysis":
        sent_icons = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}
        col1, col2 = st.columns(2)
        col1.metric("Sentiment", f"{sent_icons[result['sentiment']]} {result['sentiment']}")
        col2.metric("Confidence", f"{result['score']:.0%}")

st.divider()
st.markdown("### 📊 Batch Processing Demo")
sample_abstracts = [
    {"text": "Patient experienced severe nausea and vomiting after MRD-112.", "source": "AE Report #1047"},
    {"text": "No significant adverse events were reported during the 12-week period.", "source": "Trial Summary Q3"},
    {"text": "Elevated liver enzymes (ALT 3x ULN) observed in 12% of patients.", "source": "Safety Report"},
    {"text": "The drug demonstrated significant tumor reduction in Phase II Oncology.", "source": "Efficacy Report"},
    {"text": "Treatment discontinued due to grade 3 peripheral neuropathy.", "source": "AE Report #1089"},
]

results_batch = []
for item in sample_abstracts:
    r = analyze_text(item["text"], "Adverse Event Extraction", model_choice)
    events = r.get("events", [])
    high = len([e for e in events if e["severity"] == "HIGH"])
    results_batch.append({
        "Source": item["source"],
        "Text (preview)": item["text"][:60] + "...",
        "AE signals": len(events),
        "High severity": high,
        "Flag": "🚨" if high > 0 else "✅"
    })

df_batch = pd.DataFrame(results_batch)
st.dataframe(df_batch, use_container_width=True, hide_index=True)

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Processing Speed", "Hours → Minutes", "vs manual review")
col2.metric("Documents Processed", "Millions", "at Mentor R&D")
col3.metric("Programs Supported", "Oncology/Immuno", "drug development")
col4.metric("Compliance", "HIPAA", "fully maintained")
