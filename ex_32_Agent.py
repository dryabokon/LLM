import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
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
def ex_tools_test():
    # A1  = [159.4, -4000.0, 300.0, 191.28, 275.45, 275.45, 229.54, 229.54, 80.0, 700.0, 159.4, 191.28, 700.0, 700.0, 300.0,80.0]
    # A2 = [-4000.0, 80.0, 80.0, 159.4, 159.4, 191.28, 191.28, 229.54, 229.54, 275.45, 275.45, 300.0, 300.0, 700.0, 700.0, 700.0] #89342
    A2 = [-800.0, 300.0, 275.45, 159.4, 700.0, 191.28, 229.54]

    print(llm_tools.custom_func_IRR_calc(', '.join([str(a) for a in A2])))
    print(llm_tools.custom_func_sales_for_target_irr(A2, 0.35))
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_IRR():
    q1 = "what is IRR of a cashflow below: -100, 30, 30, 30, 30"
    q2 = "what is required sale to achieve 0.23 IRR for cashflow below: 159.4, -4000.0, 300.0, 191.28, 275.45, 275.45, 229.54, 229.54, 80.0, 700.0, 159.4, 191.28, 700.0, 700.0, 300.0, 80.0"

    #llm_cnfg = llm_config.get_config_openAI()
    llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tool_IRR()
    tools.extend(llm_tools.get_tool_sale_for_target_IRR())
    A = llm_Agent.Agent(LLM, tools,verbose=True)
    llm_interaction.interaction_offline(A, [q2], do_debug=False, do_spinner=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_pandas(df):
    query0 = 'count number of records in dataframe'
    query1 = 'what is IRR of a cashflow below: -100, 30, 30, 30, 30'
    query2 = "How many records are available for investmentID F2-ABCTech?"
    #query3 = "List first 5 records as pandas dataframe for investmentID F2-ABCTech"
    query4 = 'calculate IRR of investmentID F2-ABCTech, assuming cashflow metricName is available in Csh.'
    #query5 = 'Use available tool to evaluate required cashflow to generate for investmentID F2-ABCTech target IRR of 0.23. Assume cashflow data is encoded by metricName Csh. Do not filter out duplicates and ensure cashflow is sorted over a time.'
    query6 = 'Use available tool to evaluate required cashflow to generate for Investment_Amazon target IRR of 0.35. Assume cashflow data is encoded by metricName Csh. Do not filter out duplicates and ensure cashflow is sorted over a time.'

    q = [query6]

    llm_cnfg = llm_config.get_config_openAI()
    #llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tools_pandas(df)
    tools.extend(llm_tools.get_tool_IRR())
    tools.extend(llm_tools.get_tool_sale_for_target_IRR())
    A = llm_Agent.Agent(LLM, tools,verbose=True)
    llm_interaction.interaction_offline(A, q, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_live(df):
    llm_cnfg = llm_config.get_config_openAI()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    #A = create_pandas_dataframe_agent(LLM, df, verbose=True)
    tools = llm_tools.get_tools_pandas(df)
    tools.extend(llm_tools.get_tool_IRR())
    tools.extend(llm_tools.get_tool_sale_for_target_IRR())
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_live(A, do_spinner=False)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #df = pd.read_csv('./data/output/023de3ace6b3451082f61a3949c27239.csv')
    df = pd.read_csv('./data/output/0123.csv')
    #ex_tools_test()
    ex_agent_IRR()
    #ex_agent_pandas(df)
    #ex_live(df)



