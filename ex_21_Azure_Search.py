import pandas as pd
import tools_Azure_Search
import json
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
docs0 = [    {"hotelId": "1","hotelName": "Fancy Stay","description": "Best hotel in town if you like luxury hotels.","category": "Luxury"},
            {"hotelId": "2","hotelName": "Roach Motel","description": "Cheapest hotel in town. Infact, a motel.","category": "Budget"},
            {"hotelId": "3","hotelName": "EconoStay","description": "Very popular hotel in town.","category": "Budget"},
            {"hotelId": "4","hotelName": "Modern Stay","description": "Modern architecture, very polite staff and very clean. Also very affordable.","category": "Luxury"},
            {"hotelId": "5","hotelName": "Secret Point","description": "One of the best hotel in town. The hotel is ideally located on the main commercial artery of the city in the heart of New York.","category": "Boutique"},
        ]
# ----------------------------------------------------------------------------------------------------------------------
def ex_drop_index(index_name):
    C.search_index_client.delete_index(index_name)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_upload(docs,new_index_name):
    if new_index_name not in C.get_indices():
        C.create_search_index(docs,field_embedding=None,index_name=new_index_name)

    C.search_client = C.get_search_client(new_index_name)
    C.upload_documents(docs)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_tokenize_and_upload(docs,new_index_name,field_source='description',field_embedding='token'):

    docs_e = C.tokenize_documents(docs, field_source=field_source, field_embedding='token')
    if new_index_name not in C.get_indices():
        C.create_search_index(docs_e,'token',new_index_name)

    C.search_client = C.get_search_client(new_index_name)
    C.upload_documents(docs_e)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_search(query,index_name,select=None):

    C.search_client = C.get_search_client(index_name)
    df = C.search_semantic(query=query,select=select,as_df=True,limit=5)
    print('search_semantic')
    print(tools_DF.prettify(df, showheader=True, showindex=False))

    print('search_vector')
    df = C.search_vector(query=query,as_df=True, select=select,limit=5)
    print(tools_DF.prettify(df, showheader=True, showindex=False))

    print('search_hybrid')
    df = C.search_hybrid(query=query, as_df=True, select=select, limit=5)
    print(tools_DF.prettify(df, showheader=True, showindex=False))

    return
# ----------------------------------------------------------------------------------------------------------------------
#ex_upload(docs,new_index_name='stackoverflow123')
#C.search_index_client.delete_index('delme123')
#ex_upload(docs0,new_index_name='delme123')
#ex_tokenize_and_upload(docs0,'idxgl6_tokenized')
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #index_name = 'idxgfvect2'
    index_name = 'stackoverflow125body'
    C = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',filename_config_emb_model='./secrets/GL/private_config_azure_embeddings.yaml',index_name=index_name)
    #ex_tokenize_and_upload(json.load(open('./data/ex_datasets/stackoverflow.json', encoding="utf-8")), index_name, field_source='question_body')

    #ex_search('How is Tom?',index_name,select=['uuid','text'])

    #69044983
    ex_search('How to plot stacked bar if number of columns is not known?',index_name,select=['question_id','question_title'])

