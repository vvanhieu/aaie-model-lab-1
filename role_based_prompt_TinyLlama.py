
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Disable TensorFlow logging
os.environ["TRANSFORMERS_NO_TF"] = "1"

# ------------------------
# Load TinyLlama Model
# ------------------------
def load_tinyllama():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    text_gen = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return text_gen


# ------------------------
# AI Detection Prompt
# ------------------------
def build_ai_detection_prompt(submission: str) -> str:
    return f"""
You are an academic integrity evaluator.
Task: AI Detection.

Now analyze the NEW submission and respond in plain text with the following structure:

Label: ...
Rationale:
- point 1
- point 2
Flags: ...
NEW submission:
\"\"\"{submission}\"\"\"

Analysis:
- Point 1: The essay lacks specific examples and references, which is a clear indication that the human author was not able to conduct thorough research.
- Point 2: The text structure is clunky and shows a lack of coherence. The paragraphs are not connected, and the language is overly formal.

Label: Human

Explanation:
The student submitted their high-school essay that included a section on the social and political implications of climate change. They did a thorough job of researching and analyzing the topic, but their writing style was too formal and lacked specificity, which highlights the lack of research and analytical ability of the human author.
"""


# ------------------------
# Feedback Generation Prompt
# ------------------------
def build_feedback_prompt(submission: str) -> str:
    return f"""
You are a supportive academic assessor.
Task: Feedback Generation.

Student submission: \"\"\"{submission}\"\"\"

Assessor feedback:
Correctness: 4
Clarity: 5
Tone: 4
Actionability: 4
Coherence: 3
Emotion: 4
Overall Rating: 3.5
Feedback: "The essay provides a good overview of climate change. However, it could benefit from more specific examples and references. The author should also consider the impact of climate change on different sectors of society, such as agriculture, energy, and transportation."
Reasoning:
Correctness: The author provides a good overview of climate change, but the essay could benefit from more specific examples and references. The author should also consider the impact of climate change on different sectors of society, such as agriculture, energy, and transportation.
Clarity: The author uses clear and concise language, but there are some instances where the sentence structure could be improved. The author should also consider the impact of climate change on different sectors of society, such as
"""


# ------------------------
# Run Prompts with TinyLlama
# ------------------------
def run_prompt(pipeline, prompt: str):
    output = pipeline(prompt, max_new_tokens=600, do_sample=True, temperature=0.3)
    return output[0]["generated_text"]


# ------------------------
# Main Execution
# ------------------------
if __name__ == "__main__":
    # Load model
    generator = load_tinyllama()

    # Example submission
    submission_text = "This essay provides a good overview of climate change but lacks specific examples and references."

    # Build prompts
    detection_prompt = build_ai_detection_prompt(submission=submission_text)
    feedback_prompt = build_feedback_prompt(submission=submission_text)

    # Run tasks
    detection_result = run_prompt(generator, detection_prompt)
    feedback_result = run_prompt(generator, feedback_prompt)

    # Print results
    print("=== AI Detection Task ===")
    print(detection_result.strip())

    print("\n=== Feedback Generation Task ===")
    print(feedback_result.strip())
