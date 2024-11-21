import os
import io
import time
import pandas as pd
import tools_DF
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_RAG
from LLM2 import llm_config
# ----------------------------------------------------------------------------------------------------------------------
azure_search_index_name = 'idx_gdrive_demo'
exclude_id = '1AajLPn3vhg6z3dwTosURgarL-LcuugbQ'
# ----------------------------------------------------------------------------------------------------------------------
#llm_cnfg = llm_config.get_config_azure()
llm_cnfg = llm_config.get_config_openAI()
# ----------------------------------------------------------------------------------------------------------------------
A = llm_RAG.RAG(chain=None, filename_config_vectorstore=llm_cnfg.filename_config_vectorstore,vectorstore_index_name=azure_search_index_name,filename_config_emb_model=llm_cnfg.filename_config_emb_model)
# ----------------------------------------------------------------------------------------------------------------------
def add_file_to_index(file_id,azure_search_index_name,do_tokenize=True):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    filename_out = './' + file_id + '.txt'
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        with open(filename_out,'wb') as f:
            f.write(fh.read())


    A.add_book(filename_out, azure_search_index_name, tag=file_id, do_tokenize=do_tokenize)

    os.remove(filename_out)
    print('File downloaded and added to Azure index: ', file_id)
    return
# ----------------------------------------------------------------------------------------------------------------------
def is_indexed(file_id,azure_search_index_name):
    res = A.do_docsearch_azure(file_id, azure_search_index_name, select='uuid', limit=1)
    i=0
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    credentials = service_account.Credentials.from_service_account_file('./secrets/testproj2-bf028-1192be76a851.json', scopes=['https://www.googleapis.com/auth/drive'])
    service = build("drive", "v3", credentials=credentials)
    # A.azure_search.search_index_client.delete_index(azure_search_index_name)
    # add_file_to_index('13StiKpQ-SoR_0yLqn2eNIg44bo3jaEVZ',azure_search_index_name,do_tokenize=False)

    #is_indexed('13StiKpQ-SoR_0yLqn2eNIg44bo3jaEVZ',azure_search_index_name)



    while True:
        results = service.files().list(fields='nextPageToken, files(id, name, modifiedTime)',pageSize=10,orderBy="modifiedTime desc").execute()
        df = pd.DataFrame.from_dict(results['files'])
        df = df[df['id'] != exclude_id]
        res = tools_DF.prettify(df,showindex=False)
        print(res)
        # for file_id in df['id']:
        #     if not is_indexed(file_id,azure_search_index_name):
        #         add_file_to_index(file_id)

        time.sleep(10)  #10 sec

