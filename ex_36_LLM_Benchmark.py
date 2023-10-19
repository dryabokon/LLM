#Question Answering Challenges
#Dialogue and Conversational Agents
#Document Generation
#Question Generation
#Commonsense Reasoning
import json
import os
import numpy.linalg
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
import tools_Langchain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_LLM/squad_v2/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
def convert_data_squad(filename_in,filename_txt,filter_title=None):

    texts = []
    questions=[]
    answers=[]

    with open(filename_in, encoding="utf-8") as f:
        for example in json.load(f)["data"]:
            if filter_title is not None and example.get("title", "")!=filter_title:continue
            texts = texts + [paragraph["context"].encode(encoding='ascii', errors='ignore').decode() for paragraph in example["paragraphs"]]
            for paragraph in example["paragraphs"]:
                for qa in paragraph["qas"]:
                    questions.append(qa["question"])
                    if len(qa["answers"]) > 0:
                        answers.append(qa["answers"][0]["text"])
                    else:
                        answers.append('')

        with open(filename_txt, mode='w',encoding="utf-8") as f:
            f.write('\n'.join(texts))

    return texts,questions,answers
# ----------------------------------------------------------------------------------------------------------------------
def step_01_import_texts_to_azure(dct_config_agent,filename_in,azure_search_index_name):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA')
    A.add_document_azure(filename_in=filename_in, azure_search_index_name=azure_search_index_name)
    return
# ----------------------------------------------------------------------------------------------------------------------
def step_02_predict(dct_config_agent,azure_search_index_name,filename_out):
    texts, questions, answers_GT = convert_data_squad(folder_in + 'dev-v2.0.json', dct_book['filename_in'],filter_title=dct_book['text_key'])
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA')

    prefix = 'Answer in brief the question below. Answer as N/A if the context is not enough or information is missing.'

    if os.path.isfile(filename_out):
        os.remove(filename_out)
    for question,answer_gt in zip(questions,answers_GT):
        df = pd.DataFrame(numpy.array([question, answer_gt, A.run_chain(prefix+question, azure_search_index_name=azure_search_index_name, limit=10)]).reshape((1,3)),columns=['question','answer_gt','answer_pred'])
        if not os.path.isfile(filename_out):
            df.to_csv(filename_out, index=False)
        else:
            df.to_csv(filename_out, index=False, mode='a', header=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def step_03_evaluate_metrics(df):

    df = df.fillna('')
    tfidf_vectorizer = TfidfVectorizer()
    res=[]
    for t1,t2 in zip(df.iloc[:,1],df.iloc[:,2]):
        tfidf_matrix = tfidf_vectorizer.fit_transform([t1, t2])
        res.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))

    df['similarity'] = numpy.array(res).reshape((-1,1))

    return df
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dct_config_agent = get_config_azure()
    dct_book = {'filename_in': folder_out + 'warsaw.txt', 'text_key': 'Warsaw', 'azure_search_index_name': 'idx-warsaw','search_field': 'token', 'select': 'text'}
    #step_01_import_texts_to_azure(dct_config_agent=dct_config_agent,filename_in=dct_book['filename_in'],azure_search_index_name=dct_book['azure_search_index_name'])
    #df = step_02_predict(dct_config_agent=dct_config_agent,azure_search_index_name=dct_book['azure_search_index_name'],filename_out=folder_out+'QA.csv')
    df = pd.read_csv(folder_out+'QA.csv')
    df = step_03_evaluate_metrics(df)
    df.to_csv(folder_out+'QA2.csv', index=False)