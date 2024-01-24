import tools_Azure_Search
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
C = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',filename_config_emb_model='./secrets/GL/private_config_azure_embeddings.yaml',index_name='index1704720602307')
# ----------------------------------------------------------------------------------------------------------------------
docs0 = [    {"hotelId": "1","hotelName": "Fancy Stay","description": "Best hotel in town if you like luxury hotels.","category": "Luxury"},
            {"hotelId": "2","hotelName": "Roach Motel","description": "Cheapest hotel in town. Infact, a motel.","category": "Budget"},
            {"hotelId": "3","hotelName": "EconoStay","description": "Very popular hotel in town.","category": "Budget"},
            {"hotelId": "4","hotelName": "Modern Stay","description": "Modern architecture, very polite staff and very clean. Also very affordable.","category": "Luxury"},
            {"hotelId": "5","hotelName": "Secret Point","description": "One of the best hotel in town. The hotel is ideally located on the main commercial artery of the city in the heart of New York.","category": "Boutique"},
        ]
# ----------------------------------------------------------------------------------------------------------------------
# docs1 = [   {'id':'1',"description": "Best hotel in town if you like luxury hotels."},
#             {'id':'2',"description": "Cheapest hotel in town. Infact, a motel."},
#             {'id':'3',"description": "Very popular hotel in town."},
#             {'id':'4',"description": "Modern architecture, very polite staff and very clean. Also very affordable."},
#             {'id':'5',"description": "One of the best hotel in town. The hotel is ideally located on the main commercial artery of the city in the heart of New York."},
#         ]
# ----------------------------------------------------------------------------------------------------------------------
def ex_drop_index():
    index_name = 'idxgl2'
    C.search_index_client.delete_index(index_name)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_tokenize_and_upload():
    new_index_name = 'idxgl3'

    docs_e = C.tokenize_documents(docs0, field_source='description', field_embedding='token')

    if new_index_name not in C.get_indices():
        C.create_search_index(docs_e,'token',new_index_name)

    C.search_client = C.get_search_client(new_index_name)
    C.upload_documents(docs_e)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_search():
    index_name = 'idxgl3'
    C.search_client = C.get_search_client(index_name)
    #df = C.search_document(query='popular',select=['hotelName','category','description'])
    #df = C.search_document(query='Eco*',select=['hotelName'])
    df = C.search_document_hybrid(query='popular',field_embedding='token',select=['hotelName','category','description'])
    print(tools_DF.prettify(df, showheader=True, showindex=False))

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_search2():
    index_name = 'hotels-sample-index'
    C.search_client = C.get_search_client(index_name)
    df = C.search_document(query='pool',select=['HotelId','Description','Address'])
    texts = C.search_texts(query='pool',select=['HotelId','Description'])
    print(tools_DF.prettify(df, showheader=True, showindex=False))

    return

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #print(C.get_document(key=23))
    # C.delete_document(index_name='hotels-sample-index',dict_doc={"hotelId": "1000"})
    ex_tokenize_and_upload()
    #ex_search2()

    # C = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',filename_config_emb_model='./secrets/GL/private_config_azure_embeddings.yaml',index_name='index1704717790459')
    # docs_e = C.tokenize_documents(docs, field_source='text', field_embedding='token')
    # C.upload_documents(docs_e)