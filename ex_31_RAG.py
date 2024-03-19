from LLM2 import llm_config
from LLM2 import llm_models
from LLM2 import llm_chains
from LLM2 import llm_RAG
from LLM2 import llm_interaction
# ----------------------------------------------------------------------------------------------------------------------
dct_book1_godfather = {'filename_in': './data/ex_LLM/Godfather_2.txt', 'azure_search_index_name': 'idxgfvect2', 'search_field': 'token', 'select': 'text'}
queries1 = [ 'What was the favorite horse of the movie producer passionate about racing?',
            'How Sonny was killed ?',
            'What is Mike\'s hobby?',
            'Name 5 families of NY mafia',
            'Name all Casinos mentioned in the book',
            'Name the favorite horse of the Hollywood producer',
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
def ex_import_book(llm_cnfg, dct_book):
    A = llm_RAG.RAG(chain=None, filename_config_vectorstore=llm_cnfg.filename_config_vectorstore,vectorstore_index_name=dct_book['azure_search_index_name'],filename_config_emb_model=llm_cnfg.filename_config_emb_model)
    A.add_document_azure(dct_book['filename_in'], azure_search_index_name=dct_book['azure_search_index_name'])
    return
# ----------------------------------------------------------------------------------------------------------------------
#ex_import_book(dct_config_agent, dct_book8_TSI)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #llm_cnfg = llm_config.get_config_azure()
    llm_cnfg = llm_config.get_config_openAI()

    #ex_import_book(llm_cnfg, dct_book1_godfather)

    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    chain = llm_chains.get_chain_chat(LLM)
    dct_book = dct_book1_godfather

    A = llm_RAG.RAG(chain, filename_config_vectorstore=llm_cnfg.filename_config_vectorstore,vectorstore_index_name=dct_book['azure_search_index_name'],filename_config_emb_model=llm_cnfg.filename_config_emb_model)
    llm_interaction.interaction_offline(A,queries1,do_debug=True,do_spinner=True)
    #llm_interaction.interaction_live(A,do_debug=True,do_spinner=True)








