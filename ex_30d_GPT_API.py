#https://github.com/langchain-ai/langchain/discussions/5951
#https://python.langchain.com/docs/integrations/toolkits/openapi_nla
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
from LLM import tools_Langchain_API
# ----------------------------------------------------------------------------------------------------------------------
def get_config():
    filename_config_chat_model = './secrets/private_config_openai.yaml'
    #filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'api_spec':'https://www.klarna.com/us/shopping/public/openai/v0/api-docs/'}
    #dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'api_spec': 'spotify_API.yaml'}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    dct_config_agent = get_config()
    A = tools_Langchain_API.Assistant_API(dct_config_agent['chat_model'],dct_config_agent['api_spec'],chain_type='Summary')

    q = "Shirt options for men in blue color ordered by price."
    #q = "Give me all songs of ABBA."
    #res = A.Q_chain(q)
    # print(q)
    # print(res)

    A.Q_chain(q)














