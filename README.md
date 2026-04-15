# Email Generation Assistant — AI Engineer Assessment (Gemini Edition)

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Set up API keys
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   ```

## Run Evaluation (Model A exclusively - 1.5 Pro)
   ```bash
   python run_evaluation.py
   ```
Outputs: `outputs/evaluation_report.csv`, `outputs/model_a_results.json`

## Run Model Comparison (1.5 Pro vs 1.5 Flash)
   ```bash
   python compare_models.py
   ```
Outputs: `outputs/model_comparison.csv`, `outputs/comparative_analysis.md`, `outputs/model_b_results.json`

## Project Structure
```text
email-gen-assistant/
├── README.md                    # Setup + execution instructions
├── requirements.txt             # All dependencies
├── .env                         # API keys (never commit this)
├── .gitignore                   # Ignore .env, __pycache__, outputs/
│
├── src/
│   ├── __init__.py
│   ├── generator.py             # Core email generation logic + prompt template
│   ├── evaluator.py             # All 3 custom metric implementations
│   ├── scenarios.py             # 10 test scenarios + human reference emails
│   └── utils.py                 # Shared helpers (API call wrapper, retry logic)
│
├── run_evaluation.py            # Main script: runs all scenarios, outputs CSV/JSON
├── compare_models.py            # Runs both models, generates comparison report
│
└── outputs/                     # Contains generated evaluations
```

## Prompting Strategy
This project applies a **Role-Playing + Few-Shot + Chain-of-Thought (CoT)** approach. By assigning a Senior Business Expert persona, anchoring tone with examples, and directing a THINK->PLAN->WRITE reasoning loop before answering, the model provides higher quality and more focused business communication.

## Custom Metrics
1. **Fact Recall Score** — semantic similarity based fact checking using `sentence-transformers` models (0-100)
2. **Tone Alignment Score** — LLM-as-a-Judge tone matching leveraging `gemini-1.5-flash` cost-effectively (0-100)
3. **Fluency & Conciseness Score** — readability (using Flesch metrics) + length appropriateness vs an idealized human standard (0-100)
