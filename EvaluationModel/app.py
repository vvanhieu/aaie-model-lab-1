# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

from evaluate_model import EvaluateModel, classify_text

# --- Default Few-Shot Prompt (moved from evaluate_model.py) ---
default_prompt = """
Decide whether the following text was written by a human or an AI.
Text: "Artificial intelligence is a powerful tool for automating tasks."
Label: AI
Text: "I walked to the market this morning and bought fresh bread."
Label: Human
Text: "The moon is a celestial body that orbits Earth."
Label: AI
Text: "Yesterday, I enjoyed a long walk in the park."
Label: Human
Text: "Machine learning models improve with more data."
Label: AI
Text: "{}"
Label: Human or AI
"""

# --- Streamlit Page Config ---
st.set_page_config(page_title="Model Evaluation Dashboard", layout="wide")

# --- Page Layout ---
col_main, col_pad_right = st.columns(2)

with col_main:
    st.title("Model Evaluation Tool")

    # --- Mode Selection ---
    mode = st.selectbox("🔍 What type of model do you want to test with?", ["Classification", "Generative"])
    data_mode = st.selectbox("📂 What type of data are you using?", ["Simple Text", "JSON"])

    # --- Data Input ---
    if data_mode == "JSON":
        data = st.file_uploader("Upload dataset (JSON)", type=['json'])
    elif data_mode == "Simple Text" and mode == "Classification":
        data = st.text_area("Enter your text data (one entry per line):")
        label = st.text_input("Enter labels for the text data (comma-separated):")
    elif data_mode == "Simple Text" and mode == "Generative":
        data = st.text_area("Enter your reference and generated texts (format: ref1|gen1, ref2|gen2):")

    # --- Few-Shot Prompt ---
    prompt = st.text_area("Enter few-shot prompt:", value=default_prompt, height=150)

    # --- Options ---
    if mode == "Classification":
        avg_type = st.selectbox("Average type", ["Macro", "Micro", "Weighted", "Binary"])
    else:
        selected_metrics = st.multiselect("📏 Select metrics", ["bleu", "rouge", "bertscore"], default=["bleu", "rouge"])

    # --- Buttons ---
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        process_button = st.button("Process Model")
    with col_btn2:
        submit_button = st.button("Run Evaluation")
    with col_btn3:
        process_eval_button = st.button("Process & Evaluate")

with col_pad_right:
    dataset_preview = st.empty()
    results_container = st.container()
    matrix_container = st.container()


# --- Session State ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()


# --- Processing Logic ---
def run_processing():
    if data_mode == "JSON":
        dataset = json.load(data)
        st.session_state.df = pd.DataFrame(dataset)
        dataset_preview.write(st.session_state.df.head())
    elif data_mode == "Simple Text":
        if data.strip():
            text_data = data.splitlines()
            st.session_state.df = pd.DataFrame({"prompts": text_data, "labels": label.split(",")})
        else:
            st.error("Please enter some text data.")


# --- Evaluation Logic ---
def run_evaluation():
    if st.session_state.df.empty:
        st.error("No processed data found. Please process your data first.")
        return

    evaluator = EvaluateModel(dataset=st.session_state.df.to_dict(orient="list"))

    if mode == "Classification":
        results = evaluator.evaluate_classification_model(average=avg_type.lower())
        results_container.write("### 📊 Evaluation Results")
        results_container.write(pd.DataFrame([results]))

        # Show confusion matrix
        if "labels" in st.session_state.df.columns and "predictions" in st.session_state.df.columns:
            labels = st.session_state.df["labels"]
            preds = st.session_state.df["predictions"]
            fig, ax = plt.subplots()
            cm = pd.crosstab(labels, preds)
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("Predictions")
            ax.set_ylabel("True Labels")
            ax.set_title("Confusion Matrix")
            matrix_container.pyplot(fig)

    elif mode == "Generative":
        results = evaluator.evaluate_generative_model(metrics=selected_metrics)
        results_container.write(pd.DataFrame([results]))


# --- Button Actions ---
if process_button:
    run_processing()

if submit_button:
    run_evaluation()

if process_eval_button:
    run_processing()
    run_evaluation()
