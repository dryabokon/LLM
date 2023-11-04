import numpy
import os
import pandas as pd
# ---------------------------------------------------------------------------------------------------------------------
import tools_DF
from LLM import tools_git_analyzer
# ---------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/repo/'
repo_url = 'https://github.com/dryabokon/LLM'
# ---------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
def get_config_open_source():
    filename_config_chat_model = './secrets/private_config_openai.yaml'
    filename_config_emb_model = './secrets/private_config_openai.yaml'
    filename_config_vectorstore = './secrets/private_config_pinecone.yaml'
    dct_config={'engine':'openai','chat_model':filename_config_chat_model,'emb_model':filename_config_emb_model,'vectorstore':filename_config_vectorstore}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
# def construct_full_output(local_folder_out):
#     full_folder_out = os.getcwd()+local_folder_out
#     full_folder_out = full_folder_out.replace('.','')
#     return full_folder_out
# ---------------------------------------------------------------------------------------------------------------------
# dct_config_agent = get_config_azure()
dct_config_agent = get_config_open_source()
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('Pull request')

    A = tools_git_analyzer.Analizer_git(dct_config_agent,repo_url,folder_out)

    #print(tools_DF.prettify(A.get_repo_structure_tree(), showindex=False))
    #print(A.get_repo_structure_tree(as_txt=True))
    #print(tools_DF.prettify(A.get_history(), showindex=False))

    for i in range(A.get_history().shape[0]-1):
        print(tools_DF.prettify(A.get_diff(base=i,back=i+1), showindex=False))




