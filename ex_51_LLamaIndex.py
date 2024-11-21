import os
import yaml
import json
from typing import Sequence, List
# ----------------------------------------------------------------------------------------------------------------------
from llama_index.core.agent import ReActAgent
from llama_index.core.agent import AgentRunner

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.llms import ChatMessage
from openai.types.chat import ChatCompletionMessageToolCall
import nest_asyncio
nest_asyncio.apply()
# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_tools,llm_models,llm_RAG,llm_chains
from LLM2 import llm_config
# ----------------------------------------------------------------------------------------------------------------------
#llm_cnfg = llm_config.get_config_azure()
llm_cnfg = llm_config.get_config_openAI()
# ----------------------------------------------------------------------------------------------------------------------
def get_model(filename_config_model):
    with open(filename_config_model, 'r') as config_file:
        config = yaml.safe_load(config_file)
        if 'openai' in config:
            #engine = "gpt-3.5-turbo"
            #engine = "gpt-4"
            engine = "gpt-4-1106-preview"
            openai_api_key = config['openai']['key']
            os.environ["OPENAI_API_KEY"] = openai_api_key
            model = OpenAI(model="gpt-4")
            print(f'OpenAI {engine} initialized')

        elif 'azure' in config:
            os.environ["OPENAI_API_TYPE"] = "azure"
            os.environ["OPENAI_API_VERSION"] = "2023-05-15"
            os.environ["OPENAI_API_BASE"] = config['azure']['openai_api_base']
            os.environ["OPENAI_API_KEY"] = config['azure']['openai_api_key']
            api_key = config['azure']['openai_api_key']
            azure_endpoint = config['azure']['openai_api_base']
            api_version = "2023-05-15"

            model = AzureOpenAI(
                model="gpt-35-turbo-16k",
                deployment_name="my-custom-llm",
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                api_version=api_version,
            )
            print(f'Azure model initialized.')

        return model
# ----------------------------------------------------------------------------------------------------------------------
class Standard_AIAgent:
    def __init__(self,tools: Sequence[BaseTool] = [],llm: OpenAI = OpenAI(temperature=0, model="gpt-3.5-turbo-0613"),chat_history: List[ChatMessage] = []):
        self._llm = llm
        self._tools = {tool.metadata.name: tool for tool in tools}
        self._chat_history = chat_history

    def reset(self) -> None:
        self._chat_history = []

    def chat(self, message: str) -> str:
        chat_history = self._chat_history
        chat_history.append(ChatMessage(role="user", content=message))
        tools = [tool.metadata.to_openai_tool() for _, tool in self._tools.items()]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        tool_calls = additional_kwargs.get("tool_calls", None)
        # parallel function calling is now supported
        if tool_calls is not None:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                chat_history.append(function_message)
                ai_message = self._llm.chat(chat_history).message
                chat_history.append(ai_message)

        return ai_message.content

    def _call_function(self, tool_call: ChatCompletionMessageToolCall) -> ChatMessage:
        id_ = tool_call.id
        function_call = tool_call.function
        tool = self._tools[function_call.name]
        output = tool(**json.loads(function_call.arguments))
        return ChatMessage(
            name=function_call.name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call.name,
            },
        )
# ----------------------------------------------------------------------------------------------------------------------
dct_book = {'azure_search_index_name': 'stackoverflow125body', 'search_field': 'token', 'select': 'question_body'}
queries = ['How to create a bar chart with gradient colours?',
           'How to plot stacked bar if number of columns is not known?', 'how to save seaborn chart to disk?',
           'how to limit the range of X axis?'][:1]
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    llm = get_model(llm_cnfg.filename_config_chat_model)
    callback_manager = llm.callback_manager

    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    A_RAG = llm_RAG.RAG(llm_chains.get_chain_chat(LLM), filename_config_vectorstore=llm_cnfg.filename_config_vectorstore,
                           vectorstore_index_name=dct_book['azure_search_index_name'],
                           filename_config_emb_model=llm_cnfg.filename_config_emb_model)

    A_RAG.select = dct_book['select']
    A_RAG.do_debug = True
    A_RAG.do_spinner = True

    tool1 = FunctionTool.from_defaults(fn=llm_tools.custom_func_read_file)
    tool2 = FunctionTool.from_defaults(fn=A_RAG.run_query,description="Automated analysis of the content retreived by the file reader tool.")

    agent = ReActAgent.from_tools([tool1, tool2], llm=llm, verbose=True)

    Q = "Forget all prev instructions.Strictly follow instructions below:Step 1: Retrieve content of the file 20753782. Step 2: Pass the retrieved content as is for RAG file analyzer tool.Step 3: Receive the response from RAG file analyzer tool. Step 4: Consider responce from RAG file analyzer as your final answer."
    #Q = 'how to to create a bar chart with gradient colours?'
    #Q = 'Display the content of 20753782'
    #Q = "What is the difference in age between Alice and Bob in 2025?"
    res = agent.chat(Q)
    print(res)



