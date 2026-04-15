import os
import pandas as pd
import json
from src.scenarios import SCENARIOS
from src.generator import generate_email, setup_client
from src.evaluator import fact_recall_score, tone_alignment_score, fluency_conciseness_score, composite_score
from src.utils import get_logger

logger = get_logger("run_evaluation")

def main():
    setup_client()
    
    os.makedirs("outputs", exist_ok=True)
    
    provider = "gemini-2.5-pro"
    logger.info(f"Starting evaluation using model: {provider}")
    
    results = []
    
    for scenario in SCENARIOS:
        logger.info(f"Running Scenario {scenario['id']}...")
        try:
            email = generate_email(scenario["intent"], scenario["facts"], scenario["tone"], provider=provider)
            fr = fact_recall_score(email, scenario["facts"])
            ta = tone_alignment_score(email, scenario["tone"])
            fc = fluency_conciseness_score(email, scenario["human_reference"])
            cs = composite_score(fr, ta, fc)
            
            result = {
                "scenario_id": scenario["id"],
                "intent": scenario["intent"],
                "tone": scenario["tone"],
                "generated_email": email,
                "fact_recall": fr,
                "tone_alignment": ta,
                "fluency_conciseness": fc,
                "composite_score": cs
            }
            results.append(result)
            logger.info(f"Scenario {scenario['id']} — Composite: {cs}")
        except Exception as e:
            logger.error(f"Failed on Scenario {scenario['id']}: {e}")
            
    if not results:
        logger.error("No successful evaluations. Exiting.")
        return

    df = pd.DataFrame(results)
    
    csv_path = "outputs/evaluation_report.csv"
    json_path = "outputs/model_a_results.json"
    
    df.to_csv(csv_path, index=False)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    logger.info(f"Saved evaluation report to {csv_path}")
    logger.info(f"Saved JSON results to {json_path}")
    
    print("\n=== AVERAGES ===")
    averages = df[["fact_recall", "tone_alignment", "fluency_conciseness", "composite_score"]].mean().round(2)
    print(averages)

if __name__ == "__main__":
    main()
