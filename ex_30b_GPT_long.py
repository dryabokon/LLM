import tools_Langchain
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

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
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
def ex_import_book(dct_config_agent, dct_book):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'], dct_config_agent['vectorstore'], chain_type='QA')
    if dct_config_agent['engine']=='openai':
        A.add_document_pinecone(dct_book['filename_in'], text_key=dct_book['text_key'])
    elif dct_config_agent['engine']=='azure':
        A.add_document_azure(dct_book['filename_in'], azure_search_index_name=dct_book['azure_search_index_name'])
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(query,dct_config_agent,dct_book,do_debug=False):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA')

    if not isinstance(query,list):
        query = [query]

    for q in query:
        if dct_config_agent['engine']=='openai':
            res = A.run_chain(q, text_key=dct_book['text_key'], limit=10, do_debug=True)
        elif dct_config_agent['engine']=='azure':
            res = A.run_chain(q, azure_search_index_name=dct_book['azure_search_index_name'], limit=10, do_debug=do_debug)
        else:
            res = ''
        print(q)
        print(res)
        print(''.join(['=']*20))
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_live(dct_config_agent,dct_book,do_debug=False):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
    should_be_closed = False
    limit = 10
    while not should_be_closed:
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
                res = A.run_chain(q, text_key=dct_book['text_key'], limit=limit, do_debug=True)
            elif dct_config_agent['engine']=='azure':
                res = A.run_chain(q, azure_search_index_name=dct_book['azure_search_index_name'], search_field=dct_book['search_field'],select=dct_book['select'],limit=limit, do_debug=do_debug)
            else:
                res = ''
        except:
            res = 'Error'

        res = A.pretify_string(res)
        print(res)
        print(''.join(['='] * 20))
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dct_config_agent = get_config_azure()
    #dct_config_agent = get_config_open_source()

    #ex_import_book(dct_config_agent, dct_book5_sherlock)
    #ex_completion_offline(queries1,dct_config_agent,dct_book5_sherlock)
    ex_completion_live(dct_config_agent,dct_book5_sherlock,do_debug=False)


