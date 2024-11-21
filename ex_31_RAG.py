from LLM2 import llm_config,llm_models,llm_chains,llm_RAG,llm_interaction
import tools_Azure_Search
import tools_VertexAI_Search
# ----------------------------------------------------------------------------------------------------------------------
dct_book1_godfather = {'filename_in': './data/ex_LLM/Godfather_2.txt', 'azure_search_index_name': 'idxgfvect2', 'search_field': 'token', 'select': 'text'}
queries1 = ['Name the favorite horse of the Hollywood producer',
            'What was the favorite horse of the movie producer passionate about racing?',
            'How Sonny has ended up ?',
            'What is Mike\'s hobby?',
            'Name 5 families of NY mafia',
            'Name all Casinos mentioned in the book',
            'Who is Amerigo Bonasera?']
# ----------------------------------------------------------------------------------------------------------------------
dct_book2_HarryPotter = {'filename_in': './data/ex_LLM/HarryPotter.txt', 'text_key': 'HarryPotter', 'azure_search_index_name': 'idx-harry-potter', 'search_field': 'token', 'select': 'text'}
queries2 = [ 'Describe the game of Quidditch. What position does Harry play, and why is he particularly skilled at it?',
            'What is the Philosopher\'s Stone, and why is it important in the story ?']
# ----------------------------------------------------------------------------------------------------------------------
dct_book3_hotels = {'azure_search_index_name':'hotels-sample-index','search_field':'Description','select':['HotelId','Rating','HotelName','Description']}
# ----------------------------------------------------------------------------------------------------------------------
dct_book4_fin_report = {'filename_in': './data/ex_LLM/MBA_Fin/AVG-ANNUAL-REPORT-2022-web.pdf', 'text_key': 'Godfather','azure_search_index_name': 'index-australian-wine-annual-report', 'search_field': 'token', 'select':'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book5_sherlock = {'filename_in': './data/ex_LLM/red-headed-league.txt','azure_search_index_name':'index-sherlock','search_field': 'token', 'select': 'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book6_console_logs = {'filename_in': './data/ex_logs/Fail/47419c6b011a4fc0b19898ff72280752.txt','azure_search_index_name':'idx-log-analyzer','search_field': 'token', 'select': 'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book7_TSI = {'filename_in': './data/ex_LLM/TSI/Q-A_Session_1-Transitions_RST_CCS.pdf','azure_search_index_name':'idx-log-tsi','search_field': 'token', 'select': 'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book8_TSI = {'filename_in': './data/ex_LLM/TSI/OJ_L_2023_222_FULL_EN_TXT.pdf','azure_search_index_name':'idx-ojl','search_field': 'token', 'select': 'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book8_StackOverflow = {'azure_search_index_name':'stackoverflow125body','search_field': 'token', 'select': 'question_body'}
queries8 = ['How to create a bar chart with gradient colours?','How to plot stacked bar if number of columns is not known?','how to save seaborn chart to disk?','how to limit the range of X axis?'][:1]
# ----------------------------------------------------------------------------------------------------------------------
def ex_import_book_Azure(dct_book,rewrite=True):
    Vector_Searcher_Azure = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',index_name=dct_book['azure_search_index_name'])
    if rewrite:
        Vector_Searcher_Azure.search_index_client.delete_index(dct_book['azure_search_index_name'])
    Vector_Searcher_Azure.add_book(dct_book['filename_in'], azure_search_index_name=dct_book['azure_search_index_name'])
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_import_book_VertexAI(dct_book):
    Vector_Searcher_GCP = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')
    Vector_Searcher_GCP.add_book(dct_book['filename_in'])
    #gs_file = Vector_Searcher_GCP.add_book(dct_book['filename_in'])
    #Vector_Searcher_GCP.create_index_batch(gs_file)
    return
# ----------------------------------------------------------------------------------------------------------------------
#ex_import_book_Azure(dct_book1_godfather)
#ex_import_book_VertexAI(dct_book1_godfather)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dct_book = dct_book1_godfather

    #Vector_Searcher = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',index_name=dct_book['azure_search_index_name'])
    Vector_Searcher = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')

    #llm_cnfg = llm_config.get_config_azure()
    llm_cnfg = llm_config.get_config_GCP()

    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    chain = llm_chains.get_chain_chat(LLM)

    queries = queries1

    A = llm_RAG.RAG(chain, Vector_Searcher)
    A.select = dct_book['select']

    A.Vector_Searcher.table_name = dct_book['azure_search_index_name']
    llm_interaction.interaction_offline(A,queries,do_debug=True,do_spinner=True)
    #llm_interaction.interaction_live(A,do_debug=True,do_spinner=True)
