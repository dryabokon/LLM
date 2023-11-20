import pandas as pd
from LLM import tools_pipelines
# ----------------------------------------------------------------------------------------------------------------------
# filename_config_chat_model='./secrets/private_config_azure_chat.yaml'
filename_config_chat_model = './secrets/private_config_openai.yaml'
# ----------------------------------------------------------------------------------------------------------------------
filename_config_api='./secrets/finance/private_config_finance.yaml'
filename_api_spec='./data/ex_openapi/openai_api_spec_finance.json'
# ----------------------------------------------------------------------------------------------------------------------
P = tools_pipelines.Pipeliner(filename_config_chat_model,filename_config_api,filename_api_spec,folder_out='./data/output/')
# ----------------------------------------------------------------------------------------------------------------------
post_proc = 'Return result as pandas dataframe.Keep below columns: metricId, investmentName, reportingDate, metricName, amount, currency.'
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #df = P.query_to_df("Get all metrics limit 500.",verbose=True)
    df = pd.read_csv('./data/output/023de3ace6b3451082f61a3949c27239.csv')
    # df = P.query_over_df("What are amounts of EBITDA metrics for ABC-Tech company.",df,post_proc=post_proc)
    # df = P.query_over_df("How EBITDA metrics for ABC-Tech company has changed over the time ?",df,as_df=True)
    #df = P.query_over_df("Wha is the most attractive company for investment ?",df,as_df=False)
    P.query_over_df("Wha is the most up-to-date reporting date across companies ?",df,as_df=False)

    #df = P.query_over_df("What is IRR from financial point of view?",df,as_df=True,verbose=True)


