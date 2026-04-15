# Email Generation Assistant: Client Presentation Guide

This document is designed to help you explain the architecture, methodology, and data flow of the Email Generation Assistant project to clients or stakeholders. 

---

## 1. Executive Summary
This project is an end-to-end "AI Email Generator and Evaluator". It does not just generate emails; it rigorously tests the quality of those emails against three custom algorithms. 
The goal was to prove that we can objectively measure if an AI-generated email is factual, matches a requested tone, and sounds naturally human. We proved this by evaluating advanced Google Gemini models.

---

## 2. Project Flow (How it Works)

The pipeline operates in three distinct phases:

1. **Input Phase**: The system loads 10 unique business scenarios. Each scenario contains a specific intent (e.g., "Apologize for a missed deadline"), a set of concrete facts (e.g., "Server crashed", "New deadline is Tuesday"), and a requested tone ("Apologetic").
2. **Generation Phase**: These details are passed into the Google Gemini LLM using highly engineered prompt frameworks. The AI crafts the email.
3. **Evaluation Phase**: The generated email is intercepted and scored blindly across three completely separate metrics. Finally, a robust `.csv` and `.json` report is generated.

---

## 3. The Test Cases (Scenarios)
Rather than testing the AI randomly, we built 10 strict test scenarios located in `src/scenarios.py`. 

**Why 10 Scenarios?**
We need to see how the AI performs across varying levels of stress and contexts. The scenarios range from casual offsite invitations to high-stakes budget approvals and firm contract negotiations. 

**The Human Reference Benchmark**
For every scenario, we wrote a "Gold Standard" handwritten email. This is incredibly important. When we evaluate "How good is the AI?", the system chemically compares the AI's length, readability, and content against what a senior human manager would have actually typed.

---

## 4. Prompt Engineering Strategy

We did not just say *"Write an email"*. To get enterprise-grade output from Gemini, we used three advanced prompting techniques inside `src/generator.py`:

* **Role-Playing**: We explicitly told Gemini to act as a "Senior Business Communication Expert with 15 years of experience." This immediately raises the baseline intelligence and formatting of the output.
* **Few-Shot Prompting**: We provided the AI with a perfectly crafted example inside the prompt. This anchors the AI to understand exactly what structure we expect.
* **Chain-of-Thought (CoT)**: We forced the AI to "THINK -> PLAN -> WRITE -> CHECK" before returning the final email. This ensures the AI reasons about where to strategically place the facts before typing.

---

## 5. How We Evaluate Quality (The Metrics)

The most impressive part of this project is the `src/evaluator.py`. We built an automated grading machine that outputs a score from 0-100 based on three rules:

### A) Fact Recall Score (Accuracy)
* **What it does:** Measures if the AI hallucinated or forgot to include the provided facts.
* **How it works (Technical):** We use `SentenceTransformers` (an NLP machine learning model). We convert the facts into mathematical vectors (embeddings) and compare them to the generated email sentences using "Cosine Similarity". If a fact mathematically exists in the email, it passes.

### B) Tone Alignment Score (Emotion)
* **What it does:** Measures if the email actually sounds the way we requested (e.g., "Did making a firm contract negotiation sound too friendly?").
* **How it works (Technical):** We use a concept called "LLM-as-a-Judge". We actually spin up a second AI (`gemini-2.5-flash`), hand it the email, and force it to blindly rate the tone on a scale of 1-10. 

### C) Fluency & Conciseness Score (Readability)
* **What it does:** Ensures the email isn't a massive wall of text and doesn't sound robotic.
* **How it works (Technical):** It uses a classic linguistic formula called the *Flesch Reading Ease* test. It also calculates the strict word count of the AI email and checks it against our Handwritten Human email. If the AI writes 500 words when the human wrote 100, the AI gets heavily penalized.

---

## 6. The Multi-Model Compare System
Finally, `compare_models.py` is the ultimate testing arena. In this file, we run all 10 scenarios through a powerful model (`Gemini 2.5 Pro`) and a highly efficient model (`Gemini 2.5 Flash`) simultaneously. 

The script mathematically determines the winner and auto-generates a Markdown report `comparative_analysis.md`, which gives production recommendations on which engine is safer and cheaper to use for the company!
