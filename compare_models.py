import os
import pandas as pd
from src.scenarios import SCENARIOS
from src.generator import generate_email, setup_client
from src.evaluator import fact_recall_score, tone_alignment_score, fluency_conciseness_score, composite_score
from src.utils import get_logger

logger = get_logger("compare_models")

def run_full_evaluation(provider: str) -> pd.DataFrame:
    logger.info(f"Running full evaluation for {provider}...")
    results = []
    for scenario in SCENARIOS:
        try:
            email = generate_email(scenario["intent"], scenario["facts"], scenario["tone"], provider=provider)
            fr = fact_recall_score(email, scenario["facts"])
            ta = tone_alignment_score(email, scenario["tone"])
            fc = fluency_conciseness_score(email, scenario["human_reference"])
            cs = composite_score(fr, ta, fc)
            
            results.append({
                "scenario_id": scenario["id"],
                "intent": scenario["intent"],
                "tone": scenario["tone"],
                "generated_email": email,
                "fact_recall": fr,
                "tone_alignment": ta,
                "fluency_conciseness": fc,
                "composite_score": cs
            })
        except Exception as e:
            logger.error(f"Failed on Scenario {scenario['id']} for {provider}: {e}")
    return pd.DataFrame(results)

def compare_models(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    comparison = []
    
    for _, row_a in df_a.iterrows():
        sid = row_a["scenario_id"]
        row_b_list = df_b[df_b["scenario_id"] == sid]
        if row_b_list.empty:
            continue
        row_b = row_b_list.iloc[0]
        
        ca = row_a["composite_score"]
        cb = row_b["composite_score"]
        winner = "Model A" if ca > cb else ("Model B" if cb > ca else "Tie")
        
        comparison.append({
            "scenario_id": sid,
            "model_a_composite": ca,
            "model_b_composite": cb,
            "winner": winner
        })
        
    return pd.DataFrame(comparison)

def generate_comparative_analysis(df_a: pd.DataFrame, df_b: pd.DataFrame, comp_df: pd.DataFrame):
    avg_a = df_a[["fact_recall", "tone_alignment", "fluency_conciseness", "composite_score"]].mean().round(2)
    avg_b = df_b[["fact_recall", "tone_alignment", "fluency_conciseness", "composite_score"]].mean().round(2)
    
    def get_winner(m_a, m_b):
        return "Model A" if m_a > m_b else ("Model B" if m_b > m_a else "Tie")
    
    try:
        worst_a = df_a.loc[df_a['composite_score'].idxmin()]
        worst_b = df_b.loc[df_b['composite_score'].idxmin()]
    except Exception as e:
        logger.error(f"Error computing minimum scores: {e}")
        worst_a = {"scenario_id": "?", "composite_score": "?"}
        worst_b = {"scenario_id": "?", "composite_score": "?"}
    
    overall_winner = get_winner(avg_a['composite_score'], avg_b['composite_score'])
    
    report = f"""Title: Model Comparison Analysis — Email Generation Assistant

Models Compared:
  Model A: Gemini 2.5 Pro (gemini-2.5-pro)
  Model B: Gemini 2.5 Flash (gemini-2.5-flash)

Results Summary:
  Metric              | Model A (2.5 Pro) | Model B (2.5 Flash) | Winner
  --------------------|-------------------|---------------------|--------
  Fact Recall         | {avg_a['fact_recall']}%           | {avg_b['fact_recall']}%             | {get_winner(avg_a['fact_recall'], avg_b['fact_recall'])}
  Tone Alignment      | {avg_a['tone_alignment']}%           | {avg_b['tone_alignment']}%             | {get_winner(avg_a['tone_alignment'], avg_b['tone_alignment'])}
  Fluency/Conciseness | {avg_a['fluency_conciseness']}%           | {avg_b['fluency_conciseness']}%             | {get_winner(avg_a['fluency_conciseness'], avg_b['fluency_conciseness'])}
  Composite Score     | {avg_a['composite_score']}%           | {avg_b['composite_score']}%             | {overall_winner}

Q1: Which model performed better?
{overall_winner} performed better overall. Model A achieved a composite score of {avg_a['composite_score']} vs Model B's {avg_b['composite_score']}.

Q2: Biggest failure mode of the lower-performing model?
The worst performing scenario for Model A was Scenario {worst_a['scenario_id']} with a composite score of {worst_a['composite_score']}.
The worst performing scenario for Model B was Scenario {worst_b['scenario_id']} with a composite score of {worst_b['composite_score']}.

Q3: Production recommendation?
We recommend {overall_winner} for production due to its superior performance on the composite metrics.
"""
    with open("outputs/comparative_analysis.md", "w", encoding='utf-8') as f:
        f.write(report)
    logger.info("Saved outputs/comparative_analysis.md")


def main():
    setup_client()
    os.makedirs("outputs", exist_ok=True)
    
    model_a = "gemini-2.5-pro"
    model_b = "gemini-2.5-flash"
    
    df_a = run_full_evaluation(model_a)
    df_b = run_full_evaluation(model_b)
    
    csv_a_path = "outputs/model_a_results.json"
    csv_b_path = "outputs/model_b_results.json"
    
    df_a.to_json(csv_a_path, orient="records", indent=4)
    df_b.to_json(csv_b_path, orient="records", indent=4)
    
    comp_df = compare_models(df_a, df_b)
    comp_df.to_csv("outputs/model_comparison.csv", index=False)
    logger.info("Saved outputs/model_comparison.csv")
    
    generate_comparative_analysis(df_a, df_b, comp_df)

if __name__ == "__main__":
    main()
