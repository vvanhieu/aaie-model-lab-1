SIT378 – Project B

Project name: AAIE – LLM Prototyping and Training

**Report: Implementing Role-Based Prompting with selected model (TinyLlama) for AI Detection & Feedback Generation**


1. **Overview**

   The implementation of role-based prompting using the TinyLlama-1.1B-Chat model to perform

1) AI Detection Task: Classify student submissions as Human, AI, or Hybrid and justify based on linguistic criteria.
1) Feedback Generation Task: Generate structured academic feedback scored across six evaluation dimensions.

The goal was to test whether TinyLlama could reliably perform these roles when explicitly guided by structured role-based prompts using the evaluation criteria defined by our team.

1. **Implementation**

1. *Environment Set-up:*

- Selected Model: TinyLlama-1.1B
- Framework: Hugging Face Transformers

1. *Role-Based Prompting:*

1) **Role 1: Academic Integrity Evaluator (AI Detection):**
- Classify label the submission whether it is Human, AI, or Hybrid
- Rational: provide evidences, the reason such as grammar, cites, or lack of research.
- Explanation: provide full detail such as what student have and what they need to improve
- Flags: summary the key points (main keys)

1) **Role 2: Supportive Academic Assessor (Feedback Generation):**
- Score submission against 6 criteria (Correctness, Clarity, Tone, Actionability, Coherence, Emotion).
- Compute Overall Rating (average): show the rating from 1 to 5, such as excellent, good, average, need improvement, and poor
- Provide feedback text and reasoning for each score.

1. *Input Submission*
- The following student submission as a test input:


submission\_text = "This essay provides a good overview of climate change but lacks specific examples and references.



1. **AI Detection Output**

   1. *Expected Output format:*

`	`Label: Human | AI | Hybrid

`        `Rationale:

`       	 `- short bullet point 1

`        	`- short bullet point 2

`        `Flags: style\_inconsistency / high\_verbatim / generic\_phrasing / non

1. *Observation:*



`	`Submission: """I studied hard and wrote this essay myself."""	

`	`Label: Human

`	`Submission: """Artificial intelligence models revolutionize education by 	providing adaptive learning."""

`	`Label: AI

`	`Submission: """I asked ChatGPT for help with the outline, then expanded it 	with my own analysis."""

`	`Label: Hybrid	

`	`NEW submission:

`	`"""This essay provides a good overview of climate change, with specific 	examples and references."""

`	`Analysis:

`	`- Point 1: The essay provides a good overview of climate change, with s	pecific examples and references.

`	`- Point 2: The text structure is clunky and shows a lack of coherence. The 	paragraphs are not connected, and the language is overly formal.

`	`Label: Human

`	`Explanation:

`	`The student submitted their high-school essay that includes a section on the 	social and political implications of climate change. They did a good job of 	providing a general overview of the topic, but their writing style is too 	formal and lacking in specificity. The lack of specific examples and	 	references is also evident.

`	`Rationale:

`	`The student's lack of research and analytical ability is evident in their 	essay, which lacks specific examples and references. The lack of specificity 	in their analysis is also a clear indication of a lack of understanding of 	the topic.

`	`Flags:

`	`- The student did not conduct thorough research on the topic

- The code is success to classify the submission whether is Human, AI, or Hybrid
- The output for a few prompt testing shows the correct answer for classifying the promp.
- The output expected is flowed as an expect format, included Analysis, Label, Explanation, and Rationable.

1. **Feedback Generation Output**

   1. *Expected Output Format:*

`	`Evaluate submission against the 6 evaluation criteria:

`	`- Correctness

`	`- Clarity

`	`- Tone

`	`- Actionability

`	`- Coherence

`	`- Emotion

`	`Each scored 1–5 (1=poor, 5=excellent).



`	`Compute Overall Rating (average of all scores).

`	`Provide Feedback text.

`	`Give Reasoning (justify each criterion score).

`	`- Correctness: <justification>	

`	`- Clarity: <justification>

`	`- Tone: <justification>

`	`- Actionability: <justification>

`	`- Coherence: <justification>

`	`- Emotion: <justification>

1. *Observation:*


`	`Student submission: """This essay provides a good overview of climate change 	but Lacks specific examples and references."""

`	`Assessor feedback:

`	`- Correctness: 4

`	`- Clarity: 5

`	`- Tone: 4

`	`- Actionability: 4

`	`- Coherence: 3	

`	`- Emotion: 4

`	`- Overall Rating: 3.5

`	`Feedback: "The essay provides a good overview of climate change. However, it 	could benefit from more specific examples and references. The author should 	also consider the impact of climate change on different sectors of society, 	such as agriculture, energy, and transportation."

`	`Reasoning:

`	`- Correctness: The author provides a good overview of climate change, but 	the essay could benefit from more specific examples and references. The 	author should also consider the impact of climate change on different 	sectors of society, such as agriculture, energy, and transportation.

`	`- Clarity: The author uses clear and concise language, but there are some 	instances where the sentence structure could be improved. The author should 	also consider the impact of climate change on different sectors of society, 	such as

`	`- Clarity: The author uses clear and concise language, but there are some 	instances where the sentence structure could be improved. The author should 	also consider the impact of climate change on different sectors of society, 	such as agriculture, energy, and transportation.

`	`- Tone: The author's tone is professional and objective, but there are some 	instances where the tone could be more emotionally charged. The author 	should also consider the impact of climate change on different sectors of 	society, such as agriculture, energy, and transportation.

`	`- Actionability: The author's actionability is good, but there are some 	instances where the actionability could be improved. The author should also 	consider the impact of climate change on different sectors of society, such 	as agriculture, energy, and transportation.

`	`- Coherence: The author's coherence is good, but there are some instances 	where the coherence could be improved. The author should also consider the 	impact of climate change on different sectors of society, such as 	agriculture, energy, and transportation.

`	`- Emotion: The author's emotion is neutral, but there are some instances 	where the emotion could be more strongly expressed. The author should also 	consider the impact of climate change on different sectors of society, such 	as agriculture, energy, and transportation.

`	`Overall Rating: The essay provides a good overview of climate change. 	However, it could benefit from more specific examples and references. The 	author should also consider the impact of climate change on different 	sectors of society, such as agriculture, energy, and transportation. The 	overall rating is 3.5.

- Model followed structured scoring (from 1 - 5)
- Produced actionable, empathetic feedback for reasoning with clear explanation followed by the evaluation criteria research.
- Correctly computed Overall Rating.

