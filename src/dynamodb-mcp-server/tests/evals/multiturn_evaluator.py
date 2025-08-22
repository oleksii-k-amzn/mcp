"""
Multi-turn conversation evaluator for DynamoDB MCP tool using Strands agents.
Tests the tool through realistic interactive conversations with native MCP integration.
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os

# Strands imports
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""
    role: str  # 'user' or 'assistant' 
    content: str
    turn_number: int
    timestamp: float


@dataclass
class ConversationResult:
    """Result of a complete conversation evaluation."""
    turns: List[ConversationTurn]
    final_guidance: str
    technical_scores: Any
    # implementation_scores: Dict[str, Any]
    # practical_scores: Dict[str, Any]
    # overall_score: float


class StrandsConversationHandler:
    """Handles conversations using Strands agents with native MCP integration."""
    
    def __init__(self, model_id: str = "anthropic.claude-sonnet-4-20250514-v1:0"):
        """Initialize the Strands conversation handler."""
        self.model_id = model_id
        self.bedrock_model = BedrockModel(
            model_id=model_id,
            temperature=0.3,
            streaming=False  # Disable streaming for evaluation consistency
        )
        
    def _setup_mcp_client(self):
        """Set up the DynamoDB MCP client."""
        return MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="uv",
                args=["run", "python", "-m", "awslabs.dynamodb_mcp_server.server"],
                cwd="/Users/shetsa/workplace/mcp/src/dynamodb-mcp-server"
            ))
        )
    
    def _build_comprehensive_message(self, scenario: Dict[str, Any]) -> str:
        """Build comprehensive user message with all scenario context."""
        
        parts = [
            scenario['user_input'],
            "\nHere are the complete requirements:",
            "What type of application are you building?",
        ]
        
        # Add application details
        app_details = scenario.get('application_details', {})
        if app_details:
            parts.extend([
                f"• Type: {app_details.get('type', 'Not specified')}",
                f"• Domain: {app_details.get('domain', 'Not specified')}",
                f"• Primary Function: {app_details.get('primary_function', 'Not specified')}",
                f"• Business Model: {app_details.get('business_model', 'Not specified')}",
                ""
            ])
        
        # Add entities and relationships
        entities_rel = scenario.get('entities_and_relationships', {})
        if entities_rel:
            parts.append("What are the main entities in your system?")
            
            # Entities
            entities = entities_rel.get('entities', {})
            if entities:
                parts.append("Entities:")
                for entity, description in entities.items():
                    parts.append(f"• {entity}: {description}")
                parts.append("")
            
            # Relationships
            relationships = entities_rel.get('relationships', [])
            if relationships:
                parts.append("Relationships:")
                for relationship in relationships:
                    parts.append(f"• {relationship}")
                parts.append("")
        
        # Add access patterns
        access_patterns = scenario.get('access_patterns', {})
        if access_patterns:
            parts.append("ACCESS PATTERNS:")
            
            # Read patterns
            read_patterns = access_patterns.get('read_patterns', [])
            if read_patterns:
                parts.append("Read Patterns:")
                for pattern in read_patterns:
                    parts.append(f"• {pattern}")
                parts.append("")
            
            # Write patterns
            write_patterns = access_patterns.get('write_patterns', [])
            if write_patterns:
                parts.append("Write Patterns:")
                for pattern in write_patterns:
                    parts.append(f"• {pattern}")
                parts.append("")
        
        # Add performance and scale requirements
        perf_scale = scenario.get('performance_and_scale', {})
        if perf_scale:
            parts.append("What's the expected scale?")
            parts.append(f"• User Base: {perf_scale.get('user_base', 'Not specified')}")
            parts.append(f"• Transaction Volume: {perf_scale.get('transaction_volume', 'Not specified')}")
            parts.append(f"• Data Growth: {perf_scale.get('data_growth', 'Not specified')}")
            parts.append(f"• Read/Write Ratio: {perf_scale.get('read_write_ratio', 'Not specified')}")
            
            # Performance requirements
            perf_reqs = perf_scale.get('performance_requirements', [])
            if perf_reqs:
                parts.append("Performance Requirements:")
                for req in perf_reqs:
                    parts.append(f"• {req}")
            
            parts.extend([
                f"• Scalability Needs: {perf_scale.get('scalability_needs', 'Not specified')}", 
                f"• Regional Requirements: {perf_scale.get('regional_requirements', 'Not specified')}",
                ""
            ])
        
        # Add directive for complete guidance
        parts.extend([
            "INSTRUCTIONS:",
            "Based on this comprehensive requirements specification, please provide complete DynamoDB schema design guidance.",
            "Use the DynamoDB expert system tool to get best practices guidance, then apply it to this specific scenario.",
            "Provide detailed implementation guidance with table designs, access patterns, and capacity planning.",
            "Do not ask additional questions - provide complete guidance now."
        ])
        
        return "\n".join(parts)
    
    async def simulate_conversation(self, scenario: Dict[str, Any]) -> tuple[str, List[ConversationTurn]]:
        """
        Simulate a 2-turn conversation using Strands agent with MCP integration.
        
        Returns:
            tuple: (final_guidance, conversation_turns)
        """
        conversation = []
        start_time = time.time()
        
        try:
            # Set up MCP client for DynamoDB expert system
            dynamodb_mcp_client = self._setup_mcp_client()
            
            with dynamodb_mcp_client:
                # Get available tools from MCP server
                tools = dynamodb_mcp_client.list_tools_sync()
                
                # Create Strands agent with DynamoDB MCP tools
                agent = Agent(
                    model=self.bedrock_model,
                    tools=tools
                )
                
                # Turn 1: Initial engagement
                turn1_message = "I need help designing a DynamoDB schema. Can you help me understand your approach?"
                
                conversation.append(ConversationTurn(
                    role="user", 
                    content=turn1_message,
                    turn_number=1,
                    timestamp=time.time()
                ))
                
                turn1_response = agent(turn1_message)
                print("turn1_response: "+ str(turn1_response))
                
                conversation.append(ConversationTurn(
                    role="assistant", 
                    content=turn1_response,
                    turn_number=2,
                    timestamp=time.time()
                ))
                
                # Turn 2: Comprehensive scenario
                comprehensive_message = self._build_comprehensive_message(scenario)
                
                conversation.append(ConversationTurn(
                    role="user",
                    content=comprehensive_message, 
                    turn_number=3,
                    timestamp=time.time()
                ))
                
                turn2_response = agent(comprehensive_message).message
                print("turn2_response: "+ str(turn2_response))
                
                conversation.append(ConversationTurn(
                    role="assistant",
                    content=turn2_response,
                    turn_number=4, 
                    timestamp=time.time()
                ))
                
                return turn2_response, conversation
                
        except Exception as e:
            print(f"❌ Error during Strands conversation: {e}")
            import traceback
            traceback.print_exc()
            return f"Error during conversation: {str(e)}", conversation


class MultiTurnEvaluator:
    """Evaluates DynamoDB guidance through Strands conversations with DSPy evaluation."""
    
    def __init__(self, lm_model: str = ""):
        """Initialize the multi-turn evaluator."""
        try:
            # Use Strands for conversation handling
            self.conversation_handler = StrandsConversationHandler(lm_model)
            self.configured = True
            
            # Keep DSPy for evaluation only
            import dspy
            if not os.environ.get("AWS_DEFAULT_REGION"):
                os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
            
            # Ensure DSPy uses the same model as Strands
            dspy_model = lm_model
            
            if not dspy_model.startswith("bedrock/"):
                dspy_model = f"bedrock/{dspy_model}"
            
            dspy.configure(lm=dspy.LM(dspy_model, max_tokens=10000))
            
            from basic_evaluator import DynamoDBMCPEvaluator
            self.final_evaluator = dspy.ChainOfThought(DynamoDBMCPEvaluator)
            
        except Exception as e:
            print(f"Warning: Could not configure MultiTurnEvaluator: {e}")
            self.configured = False
    
    async def evaluate_with_conversation(self, scenario: Dict[str, Any]) -> Optional[ConversationResult]:
        """Evaluate the DynamoDB tool through a Strands conversation."""
        
        if not self.configured:
            return None
        
        try:
            # Use Strands for conversation simulation
            final_guidance, conversation = await self.conversation_handler.simulate_conversation(scenario)
            
            # Use DSPy for evaluation with expert system criteria
            final_eval = self.final_evaluator(
                user_scenario=self.conversation_handler._build_comprehensive_message(scenario),
                tool_output=final_guidance,
            )
            
            # Import the score extraction function
            from basic_evaluator import extract_numeric_score
            
            print("final_eval: " + str(final_eval))
            # Extract scores with actual field names from evaluator
            technical_scores = {
                "schema_design_quality": extract_numeric_score(str(final_eval)),
            }

           
            
            return ConversationResult(
                turns=conversation,
                final_guidance=final_guidance,
                technical_scores=technical_scores,
            )
            
        except Exception as e:
            print(f"❌ Error during evaluation: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    
    # Backward compatibility methods
    async def evaluate_dynamodb_tool(self, scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Single scenario evaluation with backward compatibility.
        Returns dict format expected by existing tests.
        """
        result = await self.evaluate_with_conversation(scenario)
        
        if result:
            return {
                "scenario_name": scenario["name"],
                # "overall_score": result.overall_score,
                "technical_scores": result.technical_scores,
                # "implementation_scores": result.implementation_scores,
                # "practical_scores": result.practical_scores,
                # "summary": {
                #     "final_guidance_length": len(result.final_guidance)
                # },
                # "evaluation_timestamp": time.time(),
                # "bedrock_response_length": len(result.final_guidance)
            }
        else:
            return {
                "scenario_name": scenario.get("name", "Unknown"),
                "error": "Strands conversation evaluation failed",
            }

    def evaluate_scenarios(self, scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.configured:
            return [{
                "error": "MultiTurnEvaluator not configured", 
                "scenario_name": scenario.get("name", "Unknown")
            }]
        
        results = []
    
        try:
            # Run async evaluation in sync context
            result = asyncio.run(self.evaluate_with_conversation(scenario))
            
            if result:
                # Convert to backward-compatible format
                compat_result = {
                    "scenario_name": scenario["name"],
                    # "overall_score": result.overall_score,
                    "technical_scores": result.technical_scores,
                    # "implementation_scores": result.implementation_scores,
                    # "practical_scores": result.practical_scores,
                    # "summary": {
                    #     "final_guidance_length": len(result.final_guidance),
                    #     "evaluation_method": "strands_mcp"
                    # },
                    # "evaluation_timestamp": time.time(),
                    # "bedrock_response_length": len(result.final_guidance)
                }
                results.append(compat_result)
            else:
                results.append({
                    "scenario_name": scenario.get("name", "Unknown"),
                    "error": "Strands conversation evaluation failed",
                    # "overall_score": None
                })
                
        except Exception as e:
            results.append({
                "scenario_name": scenario.get("name", "Unknown"),
                "error": f"Strands evaluation error: {str(e)}",
                "overall_score": None
            })
    
        return results


# Backward compatibility alias
MCPToolTester = MultiTurnEvaluator
