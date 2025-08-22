# DynamoDB MCP Server - Evaluation Framework

A comprehensive evaluation framework for testing DynamoDB data modeling guidance using DSPy and Amazon Bedrock models.

## 🚀 Quick Start

### Prerequisites

1. **AWS Credentials**: Configure AWS access for Bedrock
   ```bash
   export AWS_PROFILE=Bedrock
   # OR
   export AWS_ACCESS_KEY_ID=your_key_id
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

2. **Dependencies**: Ensure you're in the dynamodb-mcp-server directory with uv installed

### Basic Usage

```bash
# Run validation tests
uv run python simple_model_test.py

# Run basic evaluation with default model
uv run python test_dspy_evals.py

# Run with specific model
uv run python test_dspy_evals.py --model bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0

# Run comprehensive evaluation
uv run python test_dspy_evals.py --comprehensive

# Compare multiple models
uv run python test_dspy_evals.py --multi-model

# Show help
uv run python test_dspy_evals.py --help
```

## 📋 Framework Components

### Core Files

| File | Purpose |
|------|---------|
| `test_dspy_evals.py` | Main test runner with command-line interface |
| `multiturn_evaluator.py` | Enhanced 2-turn conversation evaluator |
| `basic_evaluator.py` | DSPy-based evaluation with scoring |
| `scenarios.py` | Rich test scenarios with detailed requirements |
| `multi_model_evaluator.py` | Multi-model comparison framework |

### Helper Scripts

| File | Purpose |
|------|---------|
| `simple_model_test.py` | Basic validation and import testing |
| `test_model_parameter.py` | Model parameter functionality testing |
| `example_multi_model.py` | Multi-model evaluation examples |
| `show_comprehensive_message.py` | Demo of context enhancement |

## 🎯 Key Features

### 1. Comprehensive Context Enhancement

**Problem Solved**: Models asking additional questions instead of providing complete DynamoDB guidance.

**Solution**: Enhanced Turn 2 prompt with **13.1x more context** (2,704 characters vs 206 characters).

**Before (Turn 2)**:
```
"I need to design a DynamoDB schema for an e-commerce application..."
```

**After (Turn 2)**:
```
ORIGINAL REQUEST: [user request]

APPLICATION DETAILS:
• Type: E-commerce platform
• Domain: Online retail
• Primary Function: Enable users to browse products...

ENTITIES & RELATIONSHIPS:
Entities:
• Users: Customer accounts with profile information...
• Products: Items available for purchase...

ACCESS PATTERNS:
Read Patterns:
• Get user profile by user ID (very frequent)
• List user's order history with pagination (frequent)

PERFORMANCE & SCALE REQUIREMENTS:
• User Base: 1000 active users
• Transaction Volume: 100 orders per day
• Performance Requirements:
  - Product browsing: <5ms DynamoDB response time

INSTRUCTIONS:
Based on this comprehensive requirements specification, provide complete DynamoDB schema design guidance.
Do not ask additional questions - provide complete guidance now.
```

### 2. Multi-Model Support

Compare performance across different Bedrock models:

- **Claude 3.5 Sonnet v2**: `bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Claude 3.5 Haiku**: `bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0`
- **Claude 3 Sonnet**: `bedrock/us.anthropic.claude-3-sonnet-20240229-v1:0`
- **Titan Text Premier**: `bedrock/us.amazon.titan-text-premier-v1:0`

### 3. Rich Test Scenarios

#### Simple E-commerce Schema (Beginner)
- Users, Products, Orders, OrderItems
- 1000 users, 100 orders/day
- Standard e-commerce access patterns

#### High-Scale Social Media Platform (Advanced)
- Users, Posts, Likes, Comments
- 100k+ users, 10k+ interactions/minute
- Hot partition mitigation required

#### Content Management System (Beginner)
- Authors, Articles, Categories, Comments
- 5000 page views/day, 50 articles/month
- Content organization and publishing

## 📊 Evaluation Metrics

### Technical Scores (1-10)
- **Schema Design Quality**: Table structure, key design, relationships
- **Access Pattern Coverage**: How well guidance addresses access patterns
- **Cost Optimization**: Cost-aware recommendations
- **Scalability Design**: Hot partition analysis, scaling strategies
- **Best Practices Adherence**: DynamoDB best practices compliance

### Implementation Scores (1-10)
- **Actionability**: How implementable the guidance is
- **Completeness**: Coverage of all requirements
- **Clarity**: Understandability of explanations
- **Trade-off Explanation**: Discussion of design trade-offs

### Practical Scores (1-10)
- **Scenario Fit**: Appropriateness for the use case
- **Complexity Appropriateness**: Right level of detail for user experience

## 🔧 Usage Examples

### Basic Single Model Evaluation

```bash
# Test with Claude 3.5 Haiku
uv run python test_dspy_evals.py --model bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0
```

**Sample Output**:
```json
{
  "status": "success",
  "scenarios_evaluated": 2,
  "overall_performance": {
    "average_score": 8.2,
    "score_distribution": {
      "excellent": 1,
      "good": 1,
      "acceptable": 0,
      "poor": 0
    }
  },
  "technical_performance": {
    "overall_technical_average": 8.1
  }
}
```

### Multi-Model Comparison

```bash
# Compare Claude models
uv run python test_dspy_evals.py --multi-model
```

**Sample Output**:
```json
{
  "performance_comparison": {
    "ranking": [
      {"model": "claude-3.5-sonnet-v2", "score": 8.5},
      {"model": "claude-3.5-haiku", "score": 8.2},
      {"model": "claude-3-sonnet", "score": 7.9}
    ],
    "top_performer": "claude-3.5-sonnet-v2"
  }
}
```

### Custom Model List

```python
from multi_model_evaluator import MultiModelEvaluator
from scenarios import get_scenario_by_complexity

# Define custom models
models = [
    "bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "bedrock/us.amazon.titan-text-premier-v1:0"
]

# Run evaluation
evaluator = MultiModelEvaluator(models)
scenarios = get_scenario_by_complexity("beginner")
results = evaluator.evaluate_all_models(scenarios)
```

## 🧪 Testing and Validation

### Run All Validation Tests

```bash
# Basic framework validation
uv run python simple_model_test.py

# Model parameter testing
uv run python test_model_parameter.py

# Multi-model examples (without AWS credentials)
uv run python example_multi_model.py
```

### Expected Validation Output

```
🧪 Simple Model Test - Validation Suite
==================================================

[Basic Imports]
  ✅ basic_evaluator: All items available
  ✅ scenarios: All items available
  ✅ multiturn_evaluator: All items available
  ✅ multi_model_evaluator: All items available
  ✅ test_dspy_evals: All items available

[Scenario Data]
✅ Found 3 test scenarios
  ✅ Simple E-commerce Schema: Complete structure
  ✅ High-Scale Social Media Platform: Complete structure
  ✅ Content Management System: Complete structure

[Model Configuration]
  ✅ Evaluator created with configuration status: False
  ✅ Found 4 Claude models available

[Score Extraction]
  ✅ 'Score: 8.5/10' → 8.5 (correct)
  ✅ 'Rating: 7.2 out of 10' → 7.2 (correct)

Overall: 4/4 tests passed
🎉 All validation tests passed!
```

## 🎛️ Command Line Options

```bash
uv run python test_dspy_evals.py [options]

Options:
  (no option)           Run basic evaluation with single model
  --comprehensive       Run comprehensive evaluation with all scenarios  
  --multi-model         Run evaluation across multiple Claude models
  --claude-comparison   Same as --multi-model (alias)
  --model MODEL_NAME    Specify Bedrock model to use
  --help               Show help message

Examples:
  uv run python test_dspy_evals.py
  uv run python test_dspy_evals.py --model bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0
  uv run python test_dspy_evals.py --comprehensive
  uv run python test_dspy_evals.py --multi-model
```

## 🔬 Framework Architecture

### 2-Turn Conversation Flow

1. **Turn 1**: Minimal prompt → Model asks clarifying questions
2. **Turn 2**: Comprehensive requirements → Model provides complete guidance

### Evaluation Pipeline

```
Scenario → MultiTurnEvaluator → 2-Turn Conversation → DSPy Evaluation → Scores
```

### Multi-Model Architecture

```
Scenarios → MultiModelEvaluator → [Model1, Model2, Model3] → Comparison Report
```

## 🛠️ Development and Extension

### Adding New Scenarios

Edit `scenarios.py`:

```python
new_scenario = {
    "name": "Your Scenario Name",
    "user_input": "Basic user request...",
    "complexity": "beginner|intermediate|advanced",
    "application_details": {
        "type": "Application type",
        "domain": "Domain area"
    },
    "entities_and_relationships": {
        "entities": {"Entity1": "Description"},
        "relationships": ["Entity1 → Entity2 (1:many)"]
    },
    "access_patterns": {
        "read_patterns": ["Pattern 1", "Pattern 2"],
        "write_patterns": ["Pattern 3", "Pattern 4"] 
    },
    "performance_and_scale": {
        "user_base": "Scale info",
        "performance_requirements": ["Requirement 1"]
    }
}

BASIC_SCENARIOS.append(new_scenario)
```

### Adding New Models

Edit `multi_model_evaluator.py`:

```python
# Add to COMMON_BEDROCK_MODELS
new_models = [
    "bedrock/us.meta.llama3-70b-instruct-v1:0",
    "bedrock/cohere.command-r-plus-v1:0"
]

# Add display name mapping
model_mappings = {
    "bedrock/us.meta.llama3-70b-instruct-v1:0": "llama-3-70b",
    "bedrock/cohere.command-r-plus-v1:0": "command-r-plus"
}
```

## 📈 Performance Benchmarks

### Typical Evaluation Times

- **Single Model, Single Scenario**: 15-30 seconds
- **Single Model, All Scenarios**: 45-90 seconds  
- **Multi-Model (4 models), Basic Scenarios**: 2-4 minutes

### Model Performance Patterns

Based on testing:

1. **Claude 3.5 Sonnet v2**: Highest scores, most comprehensive guidance
2. **Claude 3.5 Haiku**: Fast, good quality, cost-effective
3. **Claude 3 Sonnet**: Solid performance, detailed explanations
4. **Titan Text Premier**: Different style, competitive scores

## 🐛 Troubleshooting

### Common Issues

**"AWS credentials not available"**
```bash
# Set credentials
export AWS_PROFILE=Bedrock
# OR
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

**"Module not found" errors**
```bash
# Run from correct directory
cd src/dynamodb-mcp-server/tests/evals
uv run python test_dspy_evals.py
```

**"DSPy configuration failed"**
- Check AWS credentials have Bedrock access
- Verify model ID is correct and available in your region
- Check AWS region is set (default: us-east-1)

### Debug Mode

For detailed debugging, modify the evaluator:

```python
# In multiturn_evaluator.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📜 License

This evaluation framework is part of the DynamoDB MCP Server project and follows the same licensing terms.

## 🤝 Contributing

1. Add new test scenarios for different use cases
2. Implement additional evaluation metrics
3. Support for more Bedrock models
4. Performance optimizations for faster evaluation

## 📚 References

- [DSPy Documentation](https://dspy-docs.vercel.app/)
- [Amazon Bedrock Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
