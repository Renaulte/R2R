from core import R2RBuilder, R2RConfig
from core.agent import R2RStreamingRAGAgent
from core.base import Tool, CompletionProvider, PromptProvider, AgentConfig
from core.pipelines import SearchPipeline
import asyncio

class CustomRAGAgent(R2RStreamingRAGAgent):
    def __init__(
        self,
        llm_provider: CompletionProvider,
        prompt_provider: PromptProvider,
        search_pipeline: SearchPipeline,
        config: AgentConfig,
    ):
        super().__init__(
            llm_provider=llm_provider,
            prompt_provider=prompt_provider,
            search_pipeline=search_pipeline,
            config=config,
        )
        self.add_custom_tools()

    def add_custom_tools(self):
        calculator_tool = Tool(
            name="calculator",
            description="Perform basic arithmetic operations",
            function=self.calculate,
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation to perform",
                    },
                    "num1": {"type": "number", "description": "The first number"},
                    "num2": {"type": "number", "description": "The second number"},
                },
                "required": ["operation", "num1", "num2"],
            },
        )
        self.config.tools.append(calculator_tool)

    async def calculate(self, operation: str, num1: float, num2: float) -> str:
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return "Error: Division by zero"
            result = num1 / num2
        else:
            return "Error: Invalid operation"
        
        return f"The result of {operation} {num1} and {num2} is {result}"

# Custom agent factory
def create_custom_agent(
    llm_provider: CompletionProvider,
    prompt_provider: PromptProvider,
    search_pipeline: SearchPipeline,
    config: AgentConfig,
):
    return CustomRAGAgent(
        llm_provider=llm_provider,
        prompt_provider=prompt_provider,
        search_pipeline=search_pipeline,
        config=config,
    )

# Build custom R2R instance with the custom assistant
custom_r2r = (
    R2RBuilder(config=R2RConfig(config_data={}))
    .build()
)

# Use the custom R2R instance
async def custom_rag_agent_example():
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to a large knowledge base and a calculator."},
        {"role": "user", "content": "What's the square root of 144, and who discovered it?"},
    ]
    
    response = await custom_r2r.engine.agent(
        messages=messages,
        rag_generation_config={"max_tokens": 300, "temperature": 0.7, "stream": True},
        vector_search_settings={"use_vector_search": True, "search_limit": 5},
        kg_search_settings={"use_kg_search": True},
    )

    print("Custom RAG Agent Response:")
    async for chunk in response:
        print(chunk, end="", flush=True)
    print()

# Run the example
asyncio.run(custom_rag_agent_example())
