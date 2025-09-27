**Evaluation: Setup the Hypothesis for a goodmodel and define the Evaluation Dataset Structure for Feedback AI** 

**1. Hypothesis:** Fine-tuning a model on learner-sourced, student-written programming feedback will produce AI-generated feedback that is more accurate, useful, and stylistically closer to human student feedback than baseline models that rely only on basic or engineered prompts. 


**2. Evaluation Metrics:** We will use a combination of automatic text similarity metrics, rubric-based metrics, and human evaluations for feedback generation task.

*a) Automatic text similarity metrics:* provide quantitative comparison between AI-generated feedback and reference human feedback.

- BLEU: Measures n-gram overlap, capturing surface-level similarity.
- ROUGE-L: Measures longest common subsequence, focusing on recall and coverage.
- METEOR: Considers synonyms and stemming, making it better for semantic similarity.

Purpose: To ensure AI feedback structurally and semantically resembles human-written responses.

*b) Rubric-based alignment metrics:* We will combine binary/structural checks from prior research with a refined 6-criteria scoring rubric to better capture feedback quality.

- Correctness (Does it give accurate advice?)
- Clarity (Understandability)
- Tone (Is it supportive, non-judgmental?)
- Actionability (Does it suggest clear next steps?)
- Coherence (Is it logically structured?)
- Emotion (Does it show empathy and sensitivity?)

*c) Human Evaluation Metrics:* independent raters judge the feedback on a 5-point scale for usefulness, clarity, tone, specificity, and overall preference.

2. **Define Success Criteria:** the hypothesis states that a good model must not only generate text similar to human responses but also add value. Success criteria are:

*a) Automatic Text Similarity metrics* 
- BLUE: greater or equal 0.25. For short feedback (between 40 and 70 words), BLEU above 0.25 indicates reasonable n-gram overlap while allowing for paraphrasing. 
- ROUGE-L: greater or equal 0.35. It captures recall of important phrases; threshold set to reflect retention of key concepts in reference feedback. 
- METTOR: greater or equal 0.30. Accounts for synonym and stem matches.

*b) Rubric Metric:* a model is successful if: 
  - Automatic metrics: Meets all three thresholds for BLEU, ROUGE-L, and METEOR, and shows significant improvement over baseline prompts. 
  - Rubric metrics: Meets 5 out of 6 rubric thresholds above, with Correctness mandatory. 
    - Average ≥ 4.0/5 across all six criteria.
    - Correctness ≥ 85% alignment with human annotations.
    - Feedback length: 40–70 words (matches student style).
    - Sentence count: 2–3 sentences.

3. **Define the evaluation Dataset Structure:** we will work with data team to make sure we follow the correct format for evaluation. Assume that

*a) Dataset format and content hypothesis:*

- submission_text – student essay or response.
- generated\_feedback: text (Feedback produced by the evaluated model). 
- ground\_truth\_feedback: text (Reference feedback, such as student-written). 
- source\_type: categorical, such as "student", "AI", or "Hybrid".

*b) Rubric-Based Quality Metrics (extended criteria):
  - Correctness (Accuracy & Helpfulness): 1–5 scale.
  - Clarity (Understandability & Communication): 1–5 scale.
  - Tone (Supportiveness & Constructiveness): 1–5 scale.
  - Actionability (Clear Next Steps & Implementation): 1–5 scale.
  - Coherence (Consistency & Flow): 1–5 scale.
  - Emotion (Emotional Intelligence & Sensitivity): 1–5 scale.

**Reference:** 

1. Humanizing Automated Programming Feedback: Fine-Tuning Generative Models with Student-written feedback.  

<https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.short-papers.35/2025.EDM.short-papers.35.pdf> 



