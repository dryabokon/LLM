from LLM import tools_Langchain
# ---------------------------------------------------------------------------------------------------------------------
filename_in = './data/ex_logs/Fail/47419c6b011a4fc0b19898ff72280752.txt'
folder_out = './data/output/repo/'
# ---------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
def get_config_azure_ZS():
    filename_config_chat_model = './secrets/private_config_azure_chat_zs2.yaml'
    filename_config_emb_model = './secrets/private_config_azure_chat_zs2.yaml'
    filename_config_vectorstore = None
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
dct_config_agent = get_config_azure()
# ---------------------------------------------------------------------------------------------------------------------
A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA')
# ---------------------------------------------------------------------------------------------------------------------
def ex_01():
    query = 'Summarize the following text.'
    texts = [
        'There is a house way down in New Orleans.They call the Rising Sun.And it\'s been the ruin of many a poor boy.',
        'And God I know I\'m one.Mother was a tailor, yeah, yeah.Sewed my Levi jeans.My father was a gamblin\' man, yeah, yeah.Down, way down in New Orleans.',
        'Now the only thing a gamblin\' man ever needs.Is a suitcase, Lord, and a trunk.And the only time a fool like him is satisfied.Is when he\'s all stone cold drunk']
    res = A.chain.run(question=query, input_documents=A.texts_to_docs(texts))
    print(res)
    return
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    azure_search_index_name = 'idx-log-analyzer'
    A.add_document_azure(filename_in, azure_search_index_name=azure_search_index_name)