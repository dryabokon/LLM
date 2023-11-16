import inspect
# ---------------------------------------------------------------------------------------------------------------------
import tools_time_profiler
import tools_console_color
folder_out = './data/output/'
# ---------------------------------------------------------------------------------------------------------------------
prompt = 'Who framed Roger rabit?'
# ---------------------------------------------------------------------------------------------------------------------
TP = tools_time_profiler.Time_Profiler()
# ---------------------------------------------------------------------------------------------------------------------
def get_config_open_source():
    filename_config_chat_model = './secrets/private_config_openai.yaml'
    filename_config_emb_model = './secrets/private_config_openai.yaml'
    filename_config_vectorstore = './secrets/private_config_pinecone.yaml'
    dct_config={'engine':'openai','chat_model':filename_config_chat_model,'emb_model':filename_config_emb_model,'vectorstore':filename_config_vectorstore}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
#dct_config_agent = get_config_open_source()
dct_config_agent = get_config_azure()
# ---------------------------------------------------------------------------------------------------------------------
def test_01_LLM_OpenAI():
    from LLM import tools_LLM_OPENAI
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    A = tools_LLM_OPENAI.Assistant_OPENAILLM('./secrets/private_config_openai.yaml', folder_out)
    response = A.Q(prompt)
    print(response)
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return
# ---------------------------------------------------------------------------------------------------------------------
def test_02_LLM_Azure():
    from LLM import tools_LLM_Azure
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    A = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat.yaml', chatmode=False)
    #response = A.(prompt)
    #print(response)
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return
# ---------------------------------------------------------------------------------------------------------------------
def test_03_Langchain_context_free():
    from LLM import tools_Langchain
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
    response = A.Q(query=prompt,context_free=True)
    print(response)
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return
# ---------------------------------------------------------------------------------------------------------------------
def test_04_OPENAPI():
    from LLM import tools_Langchain_API
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    api_spec ='https://www.klarna.com/us/shopping/public/openai/v0/api-docs/'
    A = tools_Langchain_API.Assistant_API(dct_config_agent['chat_model'], api_spec=api_spec,chain_type='Summary')
    response = A.Q_chain("Shirt options for men in blue color ordered by price.")
    print(response)
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print(tools_console_color.get_test_string())
    # test_01_LLM_OpenAI()
    # test_02_LLM_Azure()
    # test_03_Langchain_context_free()
    # test_04_OPENAPI()