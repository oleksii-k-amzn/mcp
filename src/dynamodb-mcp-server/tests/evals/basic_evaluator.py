"""
Basic DSPy-based evaluator for DynamoDB data modeling guidance.
"""

import dspy
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass 
class TechnicalEvaluation:
    """Technical evaluation results."""
    schema_design_quality: str
    access_pattern_coverage: str
    cost_optimization: str
    scalability_design: str
    best_practices_adherence: str


@dataclass
class EvaluationResult:
    """Complete evaluation result."""
    overall_score: float
    technical_evaluation: TechnicalEvaluation
    summary: str
    recommendations: List[str]


class DynamoDBMCPEvaluator(dspy.Signature):
    """Evaluate DynamoDB data modeling guidance using expert criteria."""
    
    user_scenario = dspy.InputField(desc="The user's DynamoDB schema design scenario")
    tool_output = dspy.InputField(desc="The DynamoDB guidance provided by the tool")
   
    technical_evaluation = dspy.OutputField(desc="Technical quality assessment")


def extract_numeric_score(text: str) -> float:
    """Extract numeric score from evaluation text."""
    if not text:
        return 7.0  # Default fallback score
        
    # Look for patterns like "Score: 8.5" or "8.5/10" or just "8.5"
    patterns = [
        r'(?:score|rating):\s*(\d+\.?\d*)(?:/10)?',
        r'(\d+\.?\d*)/10',
        r'(\d+\.?\d*)\s*(?:out of 10|/10)',
        r'(\d+\.?\d*)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                score = float(matches[0])
                # Normalize to 1-10 scale if needed
                if score > 10:
                    score = score / 10
                return max(1.0, min(10.0, score))
            except ValueError:
                continue
    
    # Fallback: look for qualitative indicators
    text_lower = text.lower()
    if any(word in text_lower for word in ['excellent', 'outstanding', 'exceptional']):
        return 9.0
    elif any(word in text_lower for word in ['good', 'solid', 'well']):
        return 7.5
    elif any(word in text_lower for word in ['adequate', 'acceptable', 'reasonable']):
        return 6.5
    elif any(word in text_lower for word in ['poor', 'lacking', 'insufficient']):
        return 4.0
    
    return 7.0  # Default neutral score


def create_evaluation_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a comprehensive evaluation report from multiple scenario results."""
    
    if not results:
        return {
            "status": "error",
            "message": "No evaluation results provided",
            "scenarios_evaluated": 0
        }
    
    # Filter out failed scenarios
    successful_results = [r for r in results if r.get("overall_score") is not None]
    failed_results = [r for r in results if r.get("overall_score") is None]
    
    if not successful_results:
        return {
            "status": "failed",
            "message": "All scenario evaluations failed",
            "scenarios_evaluated": 0,
            "failed_scenarios": failed_results
        }
    
    # Calculate aggregate scores
    overall_scores = [r["overall_score"] for r in successful_results]
    avg_overall = sum(overall_scores) / len(overall_scores)
    
    # Aggregate technical scores
    technical_categories = ["schema_design_quality", "access_pattern_coverage", "cost_optimization", "scalability_design", "best_practices_adherence"]
    avg_technical = {}
    
    for category in technical_categories:
        scores = []
        for result in successful_results:
            tech_scores = result.get("technical_scores", {})
            if category in tech_scores and tech_scores[category] is not None:
                scores.append(tech_scores[category])
        
        if scores:
            avg_technical[category] = sum(scores) / len(scores)
        else:
            avg_technical[category] = 7.0  # Default fallback
    
    # Aggregate implementation scores  
    implementation_categories = ["actionability", "completeness", "clarity", "trade_off_explanation"]
    avg_implementation = {}
    
    for category in implementation_categories:
        scores = []
        for result in successful_results:
            impl_scores = result.get("implementation_scores", {})
            if category in impl_scores and impl_scores[category] is not None:
                scores.append(impl_scores[category])
        
        if scores:
            avg_implementation[category] = sum(scores) / len(scores)
        else:
            avg_implementation[category] = 7.0  # Default fallback
    
    # Aggregate practical scores
    practical_categories = ["scenario_fit", "complexity_appropriateness"]
    avg_practical = {}
    
    for category in practical_categories:
        scores = []
        for result in successful_results:
            prac_scores = result.get("practical_scores", {})
            if category in prac_scores and prac_scores[category] is not None:
                scores.append(prac_scores[category])
        
        if scores:
            avg_practical[category] = sum(scores) / len(scores)
        else:
            avg_practical[category] = 7.0  # Default fallback
    
    # Performance analysis
    score_distribution = {
        "excellent": len([s for s in overall_scores if s >= 9.0]),
        "good": len([s for s in overall_scores if 7.0 <= s < 9.0]),
        "acceptable": len([s for s in overall_scores if 5.0 <= s < 7.0]),
        "poor": len([s for s in overall_scores if s < 5.0])
    }
    
    return {
        "status": "success",
        "scenarios_evaluated": len(successful_results),
        "failed_scenarios": failed_results,
        "overall_performance": {
            "average_score": round(avg_overall, 2),
            "min_score": min(overall_scores),
            "max_score": max(overall_scores),
            "score_distribution": score_distribution
        },
        "technical_performance": {
            "average_scores": {k: round(v, 2) for k, v in avg_technical.items()},
            "overall_technical_average": round(sum(avg_technical.values()) / len(avg_technical), 2)
        },
        "implementation_performance": {
            "average_scores": {k: round(v, 2) for k, v in avg_implementation.items()},
            "overall_implementation_average": round(sum(avg_implementation.values()) / len(avg_implementation), 2)
        },
        "practical_performance": {
            "average_scores": {k: round(v, 2) for k, v in avg_practical.items()},
            "overall_practical_average": round(sum(avg_practical.values()) / len(avg_practical), 2)
        },
        "detailed_results": successful_results,
        "summary": f"Evaluated {len(successful_results)} scenarios with average score of {avg_overall:.2f}/10"
    }


# Example usage and testing
if __name__ == "__main__":
    # Simple test to verify the evaluator structure
    print("DynamoDB MCP Evaluator - Basic functionality test")
    print("=" * 50)
    
    # Test score extraction
    test_scores = [
        "Score: 8.5/10 - Good schema design",
        "Rating: 7.2 out of 10",
        "Excellent work - 9.1",
        "Poor implementation with score 3.5",
        "Adequate solution"
    ]
    
    print("Testing score extraction:")
    for test in test_scores:
        score = extract_numeric_score(test)
        print(f"  '{test}' -> {score}")
    
    print(f"\n✅ Basic evaluator module loaded successfully")
