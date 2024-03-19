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
#dct_config_agent = llm_config.get_config_azure()
# ----------------------------------------------------------------------------------------------------------------------
def ex_tools_test():
    # A1  = [159.4, -4000.0, 300.0, 191.28, 275.45, 275.45, 229.54, 229.54, 80.0, 700.0, 159.4, 191.28, 700.0, 700.0, 300.0,80.0]
    # A2 = [-4000.0, 80.0, 80.0, 159.4, 159.4, 191.28, 191.28, 229.54, 229.54, 275.45, 275.45, 300.0, 300.0, 700.0, 700.0, 700.0] #89342
    A2 = [-1000.0, 100.0, 200, 300, 400, 100,76]
    #A2 = [80, 80, 300, 300, 275.45, 275.45, 159.40, 159.40, 700, 700, 700, 191.28, 191.28, 229.54, 229.54,-4000]

    #print(llm_tools.custom_func_IRR_calc(', '.join([str(a) for a in A2])))
    #print(llm_tools.custom_func_sales_for_target_irr(A2, 0.05))
    print(llm_tools.pretify_output('line1\nline2\n'))

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
def ex_agent_pandas_finance(df):
    query0 = 'count number of records in dataframe'
    query1 = 'what is IRR of a cashflow below: -100, 30, 30, 30, 30'
    query2 = "How many records are available for investment Investment_Bosch?"
    query3 = "List first 5 records as pandas dataframe for Investment_Bosch"
    query4 = 'calculate IRR of Investment_Bosch, assuming cashflow metricName is available in Csh.'
    query5 = 'Use available tool to evaluate required cashflow to generate for Investment_Bosch target IRR of 0.23. Assume cashflow data is encoded by metricName Csh. Do not filter out duplicates and ensure cashflow is sorted over a time.'
    query6 = 'Evaluate required cashflow to generate for Investment_Bosch target IRR of 0.35. Assume cashflow data is encoded by metricName Csh. Do not filter out duplicates and ensure cashflow is sorted over a time.'

    q = [query4]

    llm_cnfg = llm_config.get_config_openAI()
    #llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tools_pandas_v02(df)
    tools.extend(llm_tools.get_tool_IRR())
    tools.extend(llm_tools.get_tool_sale_for_target_IRR())
    A = llm_Agent.Agent(LLM, tools,verbose=True)
    llm_interaction.interaction_offline(A, q, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_churn(df):
    q= 'according to historical dataset, what are the factors to segment/predict churn and retained customers ?'
    q = [q]

    llm_cnfg = llm_config.get_config_openAI()
    # llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tools_pandas_v02(df)
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_offline(A, q, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_pandas_automotive(df):
    #query0 = 'count number of records in dataframe'
    #query6 = 'Recommend a best value for price engine taking into account price, power, and mpg. Assume price data is encoded by price, power by  horsepower, and mpg by city-mpg.'
    #. Select top 3 cheapest.
    query6 = 'Get top 10 sorted engines demonstrating the best horsepower per city-mpg. Select 3 cheapest ones.'

    q = [query6]

    llm_cnfg = llm_config.get_config_openAI()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tools_pandas_v01(df)
    A = llm_Agent.Agent(LLM, tools,verbose=True)
    llm_interaction.interaction_offline(A, q, do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_live(df):
    llm_cnfg = llm_config.get_config_openAI()
    #llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    #A = create_pandas_dataframe_agent(LLM, df, verbose=True)
    tools = llm_tools.get_tools_pandas_v01(df)
    tools.extend(llm_tools.get_tool_IRR())
    tools.extend(llm_tools.get_tool_sale_for_target_IRR())
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_live(A, do_spinner=False)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_search():
    q = ['Who is Mr X?']

    llm_cnfg = llm_config.get_config_openAI()
    # llm_cnfg = llm_config.get_config_azure()
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    tools = llm_tools.get_tool_search()
    A = llm_Agent.Agent(LLM, tools, verbose=True)
    llm_interaction.interaction_offline(A, q, do_spinner=False)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #df = pd.read_csv('./data/output/023de3ace6b3451082f61a3949c27239.csv')
    df_finance = pd.read_csv('./data/output/Book1.csv')
    df_automotive = pd.read_csv('./data/ex_datasets/Automobile_data.csv')
    df_churn = pd.read_csv('./data/ex_datasets/dataset_churn.csv')
    # df_people = pd.read_csv('./data/EmployeeSkillsData-28-06-22--10-28.csv')
    #how many unique projects?
    #how many Senior Managers?
    #give me top 3 largest project based on number of employees

    #ex_tools_test()
    #ex_agent_IRR()
    #ex_agent_pandas_finance(df_finance)
    #ex_agent_pandas_automotive(df_automotive)
    ex_agent_churn(df_churn)
    #ex_live(df_finance)
    #ex_search()



