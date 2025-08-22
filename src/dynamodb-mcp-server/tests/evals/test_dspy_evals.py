"""
Simple DynamoDB MCP evaluation with basic functionality only.
"""

import os
import json
import time
import sys
from typing import Dict, Any

# Essential imports only
try:
    from .multiturn_evaluator import MultiTurnEvaluator as MCPToolTester
    from .basic_evaluator import create_evaluation_report
    from .scenarios import get_scenario_by_complexity, get_scenario_by_name
except ImportError:
    # Fallback for direct script execution
    from multiturn_evaluator import MultiTurnEvaluator as MCPToolTester
    from basic_evaluator import create_evaluation_report
    from scenarios import get_scenario_by_complexity, get_scenario_by_name

# Set AWS defaults
if not os.environ.get("AWS_DEFAULT_REGION"):
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

if not os.environ.get("AWS_PROFILE"):
    os.environ["AWS_PROFILE"] = "Bedrock"

# Default model - Claude 4 Sonnet in us-east-1
DEFAULT_MODEL = "anthropic.claude-sonnet-4-20250514-v1:0"


def run_basic_evaluation(model_name: str = None) -> Dict[str, Any]:
    """
    Run basic DynamoDB MCP evaluation with expert system criteria.
    
    Args:
        model_name: Bedrock model ID to use. If None, uses DEFAULT_MODEL
    
    Returns:
        Dictionary containing evaluation results
    """
    # Check for AWS credentials
    aws_available = (
        os.getenv("AWS_ACCESS_KEY_ID") is not None and 
        os.getenv("AWS_SECRET_ACCESS_KEY") is not None
    ) or os.getenv("AWS_PROFILE") is not None
    
    if not aws_available:
        return {
            "status": "skipped",
            "message": "AWS credentials not available - set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE",
            "timestamp": time.time()
        }
    
    try:
        # Use provided model or default
        selected_model = model_name or DEFAULT_MODEL
        print(f"🔄 Running DynamoDB evaluation with {selected_model}")
        
        tester = MCPToolTester(selected_model)
        
        # Run evaluation on simple e-commerce scenario
        ecommerce_scenario = get_scenario_by_name("Simple E-commerce Schema")
        print(f"📊 Testing with 'Simple E-commerce Schema' scenario")
    
        results = tester.evaluate_scenarios(ecommerce_scenario)
        
        # Generate report
        report = create_evaluation_report(results)
        report["timestamp"] = time.time()
        report["model_used"] = selected_model
        
        print("✅ Evaluation completed successfully")
        return report
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": time.time(),
            "model_used": model_name or DEFAULT_MODEL
        }


if __name__ == "__main__":
    """Simple command line interface for basic evaluation."""
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("DynamoDB MCP Basic Evaluation")
            print("=" * 40)
            print("Usage:")
            print("  python test_dspy_evals.py                    # Use default model")
            print("  python test_dspy_evals.py MODEL_NAME         # Use custom model")
            print("")
            print("Examples:")
            print("  python test_dspy_evals.py")
            print("  python test_dspy_evals.py bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0")
            print("")
            print("Requirements:")
            print("- AWS credentials (AWS_PROFILE or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY)")
            print("- Bedrock access enabled")
            sys.exit(0)
        else:
            # Custom model specified
            model_name = sys.argv[1]
            print(f"Using custom model: {model_name}")
    else:
        # Use default model
        model_name = None
        print(f"Using default model: {DEFAULT_MODEL}")
    
    # Run evaluation
    result = run_basic_evaluation(model_name)
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(json.dumps(result, indent=2))
