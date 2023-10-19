import os.path
# ---------------------------------------------------------------------------------------------------------------------
import tools_Langchain
import tools_IO
# ---------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
# ---------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ---------------------------------------------------------------------------------------------------------------------
dct_config_agent = get_config_azure()
A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
#NLP = tools_Azure_NLP.Client_NLP('./secrets/private_config_azure_NLP.yaml')
# ---------------------------------------------------------------------------------------------------------------------
def ex_01_explain(filename_in):
    text = open(filename_in).read()
    print(A.Q(query='List functions from the file for further unit testing.', context_free=True, texts=text))

    return
# ---------------------------------------------------------------------------------------------------------------------
def ex_02_write_unit_test(filename_in,folder_out):
    if os.path.isfile(filename_in):
        with open(filename_in,mode='r') as f:
            texts = f.read()
        function_name = 'json_to_pandas_v01'

        for i, scanario in enumerate(['Edge Cases']):
            query = f'Construct a python file routine with one unit test for function {function_name} so it can be executed in with single command in console.' \
                    f'Focus on testing the logic to cover the {scanario} scenario.'

            res = A.Q(query=query, context_free=True, texts=[texts])
            with open(folder_out+'test_%02d.py'%i,mode='w') as f:
                f.write(res)
    return
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    tools_IO.remove_files(folder_out,list_of_masks='*.py')
    filename_in = './ex_01a_unit_tests_codebase.py'
    #ex_01_explain(filename_in)
    ex_02_write_unit_test(filename_in,folder_out)