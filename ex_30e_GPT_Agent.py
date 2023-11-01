# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
import tools_Langchain_Agent
# ----------------------------------------------------------------------------------------------------------------------
def get_config():

    # filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    # filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    # filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    filename_config_chat_model = './secrets/private_config_openai.yaml'
    filename_config_emb_model = './secrets/private_config_openai.yaml'
    filename_config_vectorstore = './secrets/private_config_pinecone.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model,'vectorstore': filename_config_vectorstore}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    dct_config_agent = get_config()
    A = tools_Langchain_Agent.Agent(dct_config_agent['chat_model'], chain_type='API')
    #q = "6+8=?"
    q = "Shirt options for men in blue color."
    res = A.Q(q)
    print(q)
    print(res)











