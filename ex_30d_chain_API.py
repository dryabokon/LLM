#https://github.com/langchain-ai/langchain/discussions/5951
#https://python.langchain.com/docs/integrations/toolkits/openapi_nla
# ----------------------------------------------------------------------------------------------------------------------
import io
import yaml
import pandas as pd
import requests
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
import tools_DF
from LLM2 import llm_config
from LLM2 import llm_models
from LLM2 import llm_chains
# ---------------------------------------------------------------------------------------------------------------------
def yaml_to_json(text_yaml):
    io_buf = io.StringIO()
    io_buf.write(text_yaml)
    io_buf.seek(0)
    res_json = yaml.load(io_buf, Loader=yaml.Loader)
    return res_json
# ---------------------------------------------------------------------------------------------------------------------
def parse_responce(response,list_of_columns=['name','Color','Material','price']):
    dct_res = yaml_to_json(response)['products']
    df = pd.DataFrame.from_dict(dct_res)
    df_a = pd.DataFrame([])
    for r in range(df.shape[0]):
        attributes = df['attributes'].iloc[r]
        dct_a = dict(zip([a.split(':')[0] for a in attributes], [a.split(':')[-1] for a in attributes]))
        df_a = pd.concat([df_a,pd.DataFrame.from_dict([dct_a])])

    df = pd.concat([df.reset_index().iloc[:,1:], df_a.reset_index().iloc[:,1:]], axis=1)
    df = df[list_of_columns]
    response = tools_DF.prettify(df, showindex=False)

    return response
# ---------------------------------------------------------------------------------------------------------------------
def ex_new():
    llm_cnfg = llm_config.get_config_openAI()
    #api_spec = 'https://www.klarna.com/us/shopping/public/openai/v0/api-docs/'
    api_spec = './data/ex_openapi/openai_api_spec_finance.json'
    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    chain = llm_chains.get_chain_API(LLM,api_spec)
    #q = "Shirt options for men in blue color ordered by price."
    q = "load all records limit 500"

    payload_predict = chain.api_request_chain.predict(question=q,api_docs=llm_chains.get_api_spec(api_spec, format='txt'))
    print(payload_predict)
    payload_predict = payload_predict.split()[0]
    response = requests.get(payload_predict)
    df = parse_responce(response.text)
    print(tools_DF.prettify(df, showindex=False))

    return
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    ex_new()