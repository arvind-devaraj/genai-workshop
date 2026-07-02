import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# =====================================================================
# 1. Initialize Together.ai Model with Pydantic AI 2.x Architecture
# =====================================================================

# Fetch API key from your environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise ValueError(
        "Missing TOGETHER_API_KEY! Please set it in your environment: \n"
        "export TOGETHER_API_KEY='your_actual_key_here'"
    )

# Using OpenAIChatModel pointing directly to Together.ai's gateway
# (Together.ai only supports the /v1/chat/completions endpoint, not /v1/responses)
together_model = OpenAIChatModel(
    model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    provider=OpenAIProvider(
        base_url="https://api.together.xyz/v1",
        api_key=TOGETHER_API_KEY
    )
)


# =====================================================================
# 2. Define the Target Extraction Schema
# =====================================================================
class ResearchSummary(BaseModel):
    topic: str = Field(
        description="The localized primary topic or entity being researched."
    )
    key_findings: list[str] = Field(
        description="A curated list of critical milestones, recent events, or data points discovered."
    )
    unresolved_questions: list[str] = Field(
        description="Contradictions, lack of clear metrics, or items requiring further investigation."
    )
    executive_synthesis: str = Field(
        description="A cohesive 2-3 sentence technical takeaway wrapping up the state of the domain."
    )


# =====================================================================
# 3. Create the Type-Safe Agent
# =====================================================================
research_agent = Agent(
    model=together_model,
    output_type=ResearchSummary,                   # Enforces structural runtime validation
    tools=[duckduckgo_search_tool(max_results=5)], # Registers search capabilities
    system_prompt=(
        "You are a rigorous, no-nonsense research engineer. Your task is to use "
        "the provided web search tool to gather the latest telemetry, data, and context "
        "on the user's query. Filter out marketing fluff and synthesize structural truths "
        "directly into the requested format."
    )
)


# =====================================================================
# 4. Driver Execution Loop
# =====================================================================
if __name__ == "__main__":
    # Define an active topic
    target_topic = "What is the current industry consensus on using GRPO over PPO for model alignment?"
    
    print(f"📡 Initializing search queries for: '{target_topic}'...\n")
    
    # Synchronous execution run
    result = research_agent.run_sync(target_topic)
    
    # The output is fully resolved and native to our Pydantic schema
    summary: ResearchSummary = result.output
    
    # Display the structured payload
    print(f"## Topic: {summary.topic}\n")
    
    print("### 🔍 Key Findings:")
    for finding in summary.key_findings:
        print(f"  - {finding}")
        
    print("\n### ⚠️ Conflicting Details / Caveats:")
    for question in summary.unresolved_questions:
        print(f"  - {question}")
        
    print(f"\n### 🎯 Technical Synthesis:\n{summary.executive_synthesis}")