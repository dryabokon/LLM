import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_interaction
from LLM2 import llm_config
from LLM2 import llm_models
from LLM2 import llm_tools
from LLM2 import llm_Agent
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
dct_config_agent = llm_config.get_config_azure()
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_custom1():
    q1 = "what is IRR of a cashflow below: -100, 30, 30, 30, 30"

    llm_cnfg = llm_config.get_config_openAI()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tool_IRR()
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_offline(A, q1, do_debug=True, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_custom2():
    q1 = "What is the difference in age between Alice and Bob in 2025?"

    llm_cnfg = llm_config.get_config_openAI()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tool_age_of_Alice()
    #tools.extend(llm_tools.get_tool_age_of_Bob())
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_offline(A, q1, do_debug=True, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    ex_agent_custom2()
