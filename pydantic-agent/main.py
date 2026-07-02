import ast
import operator
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, ModelSettings
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

# 1. The model the agent will reason with.
# parallel_tool_calls=False makes the model wait for a tool's result before
# deciding what to do next -- without it, this model calls a tool and
# writes its final answer in the same turn, before it has read the tool's
# result, and ends up making things up.
model = OpenAIChatModel(
    model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    provider=OpenAIProvider(
        base_url="https://api.together.xyz/v1",
        api_key=os.environ["TOGETHER_API_KEY"],
    ),
    settings=ModelSettings(parallel_tool_calls=False),
)


# 2. The shape we want the final answer in. Kept generic (not tied to
# specific fields like "amazon_price") so the same agent can answer any
# price/discount question, not just one fixed comparison.
class Answer(BaseModel):
    answer: str = Field(description="A direct answer to the question, including the final numeric result")
    reasoning: str = Field(description="The numbers used and how they were combined to reach the answer")
    sources: list[str] = Field(description="The actual URLs used to find prices, not platform names")


agent = Agent(
    model=model,
    output_type=Answer,
    tools=[duckduckgo_search_tool(max_results=3)],
    system_prompt=(
        "Use search to find the current price -- do not answer from memory. "
        "Use the calculate tool for every arithmetic step (addition, subtraction, "
        "multiplication, division). Deciding which of two numbers is smaller, e.g. for "
        "a capped discount, you can do yourself without the tool."
    ),
)


# 3. A second tool, for a different reason than the search tool above: the
# model isn't reliable at arithmetic, so instead of letting it compute
# amounts in its head, we give it a tool that computes an exact answer --
# restricted to arithmetic only, since it's fed model output.
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
_UNARY_OPS = {ast.USub: operator.neg}


def _eval(node: ast.expr) -> float:
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    raise ValueError("only +, -, *, /, parentheses and numbers are supported -- no functions or commas")


@agent.tool_plain(retries=3)
def calculate(expression: str) -> float:
    """Evaluate an arithmetic expression, e.g. '79900 - 1500'.

    Only +, -, *, / and parentheses are supported -- no comparisons like
    '<' or '>'. To find the smaller of two numbers, just compare them yourself.
    """
    # Raising ModelRetry (rather than letting the ValueError below escape) lets
    # the model see the error and retry with a fixed expression instead of
    # crashing the whole run on a single malformed tool call.
    try:
        return _eval(ast.parse(expression, mode="eval").body)
    except (ValueError, SyntaxError) as e:
        raise ModelRetry(f"Could not evaluate '{expression}': {e}") from e


if __name__ == "__main__":
    question = (
        "Check the current price of a 128GB iPhone 15 on Amazon India. If I pay using "
        "an SBI Credit Card, there is an instant 10% discount but it is capped at a "
        "maximum of ₹1,500. Calculate my exact final billing amount."
    )
    result = agent.run_sync(question)

    print(result.output.answer)
    print(f"\nReasoning: {result.output.reasoning}")
    print("\nSources:")
    for source in result.output.sources:
        print(f"- {source}")
