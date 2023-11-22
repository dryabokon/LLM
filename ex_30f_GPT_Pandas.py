import pandas as pd
import tools_DF
from LLM import tools_pipelines
import tools_console_color
# ----------------------------------------------------------------------------------------------------------------------
# filename_config_chat_model='./secrets/private_config_azure_chat.yaml'
filename_config_chat_model = './secrets/private_config_openai.yaml'
# ----------------------------------------------------------------------------------------------------------------------
filename_config_api='./secrets/finance/private_config_finance.yaml'
filename_api_spec='./data/ex_openapi/openai_api_spec_finance.json'
# ----------------------------------------------------------------------------------------------------------------------
#df = P.query_over_df("What are amounts of EBITDA metrics for F2-ABCTech company in 2020.",df,post_proc=post_proc)
#df = P.query_over_df("How much maximum and minimum EBITDA metrics vary for F2-ABCTech company in 2020 ?",df,as_df=True)
#df = P.query_over_df("Wha is the most attractive company for investment ?",df,as_df=False)
#P.query_over_df("Wha is the most up-to-date reporting date across companies ?",df,as_df=False)
#df = P.query_over_df("What is IRR from financial point of view?",df,as_df=True,verbose=True)
# ----------------------------------------------------------------------------------------------------------------------
P = tools_pipelines.Pipeliner(filename_config_chat_model,filename_config_api,filename_api_spec,folder_out='./data/output/')
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(P):
    P.query_agent("How many records are available for F2-ABCTech company?")
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_live(P,df):

    should_be_closed = False
    while not should_be_closed:
        print(tools_console_color.apply_style('>','GRN'),end='')
        query = input()
        if len(query)==0:
            should_be_closed = True
            continue

        res = P.query_over_df(query,df,verbose=False)

        if isinstance(res, pd.DataFrame):
            print(tools_DF.prettify(res, showindex=False))
        else:
            print(P.A.pretify_string(res))
        print('')

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    df = P.query_to_df("Get all records limit 100.",verbose=True)
    ex_completion_live(P,df)

