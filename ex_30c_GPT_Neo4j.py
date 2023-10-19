#https://neo4j.com/developer-blog/harness-large-language-models-neo4j/
#https://neo4j.com/developer-blog/langchain-cypher-search-tips-tricks/
# ----------------------------------------------------------------------------------------------------------------------
import json
import pandas as pd
import numpy
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
import tools_Langchain
import tools_neo4j
# ----------------------------------------------------------------------------------------------------------------------
filename_config_neo4j = './secrets/private_config_neo4j.yaml'
filename_config_ssh = './secrets/private_config_ssh.yaml'
NEO4J = tools_neo4j.processor_Neo4j(filename_config_neo4j,filename_config_ssh,folder_out)
# ----------------------------------------------------------------------------------------------------------------------
def get_config_neo4j():
    filename_config_neo4j = './secrets/private_config_neo4j.yaml'
    # filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    # filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    # filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    filename_config_chat_model = './secrets/private_config_openai.yaml'
    filename_config_emb_model = './secrets/private_config_openai.yaml'
    filename_config_vectorstore = './secrets/private_config_pinecone.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model,'vectorstore': filename_config_vectorstore,'neo4j': filename_config_neo4j}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
def prepare_dataset_titanic(flat_struct_for_classification=True):
    filename_in = folder_in + 'dataset_titanic.csv'
    df = pd.read_csv(filename_in, sep='\t')
    df.drop(columns=['alive', 'deck'], inplace=True)
    df['ID']=numpy.arange(df.shape[0])
    #df = tools_DF.hash_categoricals(df)
    df = df.dropna()
    #df = df.astype(int)
    target = 'survived'

    if flat_struct_for_classification:
        dct_entities = {'Person': ['ID', 'age','sex', 'who', 'adult_male','embark_town', 'embarked','parch', 'alone','sibsp','pclass', 'class','fare',target]}
        dct_relations = {'ORG': ['Person', 'Person']}
    else:
        dct_entities = {'Person': ['ID','age',target],
                        'Gender': ['sex', 'who', 'adult_male'],
                        'Location': ['embark_town', 'embarked'],
                        'Family': ['parch', 'alone','sibsp'],
                        'Cabin':['pclass', 'class','fare']
                        }
        dct_relations = {'ORG': ['Person', 'Location'],
                         'GND': ['Person', 'Gender'],
                         'FAM': ['Person', 'Family'],
                         'CAB': ['Person', 'Cabin'],
                         }

    features_classification = [f for f in dct_entities[[k for k in dct_entities.keys()][0]] if f!=target]

    return df,dct_entities,dct_relations,features_classification,target
# ----------------------------------------------------------------------------------------------------------------------
def prepare_dataset_hotels():
    filename_in = folder_in + 'hotels.json'
    with open(filename_in, 'r') as f:
        dct = json.load(f)

    fields = ['HotelId', 'HotelName', 'Description','Category','Rating','ParkingIncluded','Address']
    res = [[d[k] for k in fields] for d in dct['value']]
    df = pd.DataFrame(res,columns=fields)
    df['Address'] = df['Address'].apply(lambda x: x['City'])

    dct_entities = {'Hotel': ['HotelId', 'HotelName','Description','ParkingIncluded'],
                    'Category': ['Category'],
                    'Address':['Address'],
                    'Rating': ['Rating'],
                    }
    dct_relations = {'HCT': ['Hotel', 'Category'],
                     'HRT': ['Hotel', 'Rating'],
                     'HLC': ['Hotel', 'Address'],
                     'CRT': ['Category', 'Rating'],
                     'CLC': ['Category', 'Address'],
                     'LCR': ['Address', 'Rating']
                     }

    target = 'Rating'
    features_classification = [f for f in dct_entities[[k for k in dct_entities.keys()][0]] if f!=target]
    return df,dct_entities,dct_relations,features_classification,target
# ----------------------------------------------------------------------------------------------------------------------
def export_to_neo4j_titanic():
    df, dct_entities, dct_relations, features, target = prepare_dataset_titanic(flat_struct_for_classification=False)
    NEO4J.export_df_to_neo4j(df, dct_entities, dct_relations, drop_if_exists=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
def export_toneo4j_hotels():
    df, dct_entities, dct_relations, features, target = prepare_dataset_hotels()
    filename_tmp = 'hotels.json'
    NEO4J.df_to_json(df, filename_tmp)
    NEO4J.export_json_to_neo4j(filename_tmp, dct_entities, dct_relations, drop_if_exists=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(query,dct_config_agent):
    # query = "How many survived males aged 50+ from Southampton?"
    # query = "how many woman aged 50+ from Southampton has survived"
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], filename_config_neo4j=dct_config_agent['neo4j'],chain_type='Neo4j')
    res = A.chain.run(query)
    print(query, res)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_live(dct_config_agent):
    A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'],filename_config_neo4j=dct_config_agent['neo4j'], chain_type='Neo4j')
    should_be_closed = False
    prefix = ''
    # prefix = 'Evaluate below request so it directly can query the Neo4j and provide robust response. ' \
    #          'Keep in mind, the relationship in base are:  Person-Cabin, Person-Family, Person-Gender, Person-Location. No other relationships available.' \
    #          'Make assumptions if needed.make sure your prompt complies with cypher syntax before executing it.\n\n'

    while not should_be_closed:
        q = input()
        if len(q)==0:
            should_be_closed = True

        try:
            res = A.chain.run(prefix+q)
            #res = A.pretify_string(res)
            print(res)
            print(''.join(['='] * 20))
        except:
            print('Error')

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #export_toneo4j_hotels()

    dct_config_agent = get_config_neo4j()

    #query = "How many survived males from Southampton?"
    #query = "how many woman aged 50+ from Southampton has survived"
    #ex_completion_offline(query, dct_config_agent)

    ex_completion_live(dct_config_agent)

    NEO4J.close()







