from LLM import tools_Langchain
# ----------------------------------------------------------------------------------------------------------------------
import tools_console_color
# ----------------------------------------------------------------------------------------------------------------------
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
    filename_config_NLP = './secrets/private_config_azure_NLP.yaml'
    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True,'NLP':filename_config_NLP}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
dct_book1_godfather = {'filename_in': './data/ex_LLM/Godfather.txt', 'text_key': 'Godfather', 'azure_search_index_name': 'idx-godfather-v02', 'search_field': 'token', 'select': 'text'}
queries1 = [ 'What was the favorite horse of the movie producer and passionate about racing?',
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
def ex_import_book(dct_config_agent, dct_book):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'], dct_config_agent['vectorstore'], chain_type='QA')
    if dct_config_agent['engine']=='openai':
        A.add_document_pinecone(dct_book['filename_in'], text_key=dct_book['text_key'])
    elif dct_config_agent['engine']=='azure':
        A.add_document_azure(dct_book['filename_in'], azure_search_index_name=dct_book['azure_search_index_name'])
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(query,dct_config_agent,dct_book,do_debug=False):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'],filename_config_NLP=dct_config_agent['NLP'], chain_type='QA')

    if not isinstance(query,list):
        query = [query]

    for q in query:
        if dct_config_agent['engine']=='openai':
            res,texts = A.run_chain(q, text_key=dct_book['text_key'], limit=10)
        elif dct_config_agent['engine']=='azure':
            res,texts = A.run_chain(q, azure_search_index_name=dct_book['azure_search_index_name'], limit=10)
        else:
            res,texts = '',[]

        print(tools_console_color.apply_style(q,is_bold=True))
        print(res)
        if do_debug:
            res_short = A.Q(res + 'Question: ' + query[0] + 'Answer as named entity.', context_free=True).replace('.', '')
            for t in texts:
                t = tools_console_color.apply_style(t, color='gray')
                t = tools_console_color.highlight_words(t,res_short)
                print(t)
                print(tools_console_color.apply_style(''.join(['-']*20),color='gray'))

        print(''.join(['=']*20))
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_live(dct_config_agent,dct_book,do_debug=False):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
    should_be_closed = False
    limit = 4
    while not should_be_closed:
        print('>',end='')
        q = input()
        if len(q)==0:
            should_be_closed = True
        if q == 'debug on':
            do_debug = True
            continue
        if q == 'debug off':
            do_debug = False
            continue
        if q.find('limit') ==0:
            limit = int(q.split(' ')[-1])
            continue

        try:
            if dct_config_agent['engine']=='openai':
                res,texts = A.run_chain(q, text_key=dct_book['text_key'], limit=limit)
            elif dct_config_agent['engine']=='azure':
                res,texts= A.run_chain(q, azure_search_index_name=dct_book['azure_search_index_name'], search_field=dct_book['search_field'],select=dct_book['select'],limit=limit)
            else:
                res,texts = '',[]
        except:
            res,texts = 'Error',[]

        res = A.pretify_string(res)
        print(res)

        if do_debug:
            #res_short = A.Q(res + 'Question: ' + q + 'Answer as named entity.', context_free=True).replace('.', '').split()
            for t in texts:
                t = tools_console_color.apply_style(t, color='gray')
                #t = tools_console_color.highlight_words(t,res_short)
                print(A.pretify_string(t))
                print(tools_console_color.apply_style(''.join(['-']*20),color='gray'))

        print(''.join(['='] * 20))
    return
# ----------------------------------------------------------------------------------------------------------------------
def pdf2text():
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
    texts = A.pdf_to_texts('./data/ex_LLM/Godfather2.pdf')
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dct_config_agent = get_config_azure()
    #ex_import_book(dct_config_agent, dct_book8_TSI)
    #queries = ['How section 6.%d is named? Give exact short answer.' % i for i in range(57)]

    #ex_completion_offline(queries,dct_config_agent,dct_book8_TSI,do_debug=False)
    ex_completion_live(dct_config_agent,dct_book6_console_logs,do_debug=True)




