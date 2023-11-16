# ---------------------------------------------------------------------------------------------------------------------
import tools_DF
from LLM import tools_git_analyzer
# ---------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/repo/'
#repo_url = 'https://github.com/dryabokon/tools'
#repo_url = 'https://github.com/numpy/numpy.git'
repo_url = 'https://github.com/openai/openai-python'
#repo_url = 'https://github.com/astanin/python-tabulate'
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
#dct_config_agent = get_config_azure()
dct_config_agent = get_config_open_source()
# ---------------------------------------------------------------------------------------------------------------------
A = tools_git_analyzer.Analizer_git(dct_config_agent,repo_url,folder_out)
# ---------------------------------------------------------------------------------------------------------------------
def ex_repo_structure():
    #print(A.get_repo_structure_tree(as_txt=True))
    print(tools_DF.prettify(A.get_repo_structure_tree(), showindex=False))
    return
# ---------------------------------------------------------------------------------------------------------------------
def ex_history():
    print(tools_DF.prettify(A.get_history(max_count=15), tablefmt='grid',showindex=False,maxcolwidths=45))
    return
# ---------------------------------------------------------------------------------------------------------------------
def ex_stats_incremental(create_patch=True):
    for i in range(7):
        print(tools_DF.prettify(A.get_diff(base=i,back=i+1, create_patch=create_patch), tablefmt='grid' if create_patch else 'psql', showindex=False,maxcolwidths=80))
    return
# ---------------------------------------------------------------------------------------------------------------------
def summarize_commit():
    print(tools_DF.prettify(A.summarize_commit(base=1,back=3, detailed=True), tablefmt='grid', showindex=False,maxcolwidths=30))
    return
# ---------------------------------------------------------------------------------------------------------------------
def summarize_commits():
    print(tools_DF.prettify(A.summarize_commits(max_count=9), tablefmt='grid', showindex=False,maxcolwidths=30))
    return
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # ex_history()
    #ex_stats_incremental()
    summarize_commit()
    #summarize_commits()





