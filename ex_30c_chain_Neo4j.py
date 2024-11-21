#https://neo4j.com/developer-blog/harness-large-language-models-neo4j/
#https://neo4j.com/developer-blog/langchain-cypher-search-tips-tricks/
# ----------------------------------------------------------------------------------------------------------------------
import json
import pandas as pd
import numpy
import tools_neo4j
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_interaction
from LLM2 import llm_config
from LLM2 import llm_models
from LLM2 import llm_chains
# ----------------------------------------------------------------------------------------------------------------------
filename_config_neo4j = './secrets/private_config_neo4j_local.yaml'
filename_config_ssh = './secrets/private_config_ssh.yaml'
NEO4J = tools_neo4j.processor_Neo4j(filename_config_neo4j,filename_config_ssh,folder_out)
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
def prepare_dataset_automotive():
    df = pd.read_csv(folder_in + 'Automobile_data.csv')

    df['ID']=numpy.arange(df.shape[0])
    df = df.dropna()

    dct_entities = {'Vehicle': ['make'],
                    'Engine': ['engine_size', 'num_of_cylinders','compression_ratio'],
                    'Power': ['horsepower'],
                    'Price':['price']
                    }
    dct_relations = {'ORG': ['Vehicle', 'Engine'],
                     'PWR': ['Vehicle', 'Power'],
                     'ENG': ['Engine', 'Power'],
                     }

    features_classification = []

    return df,dct_entities,dct_relations,features_classification,''
# ----------------------------------------------------------------------------------------------------------------------
def prepare_dataset_telecom():
    df = pd.read_csv(folder_in + './WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df = df.dropna()
    target = 'Churn'
    dct_entities = {'Customer': ['customerID',target],
                    'Demographics': ['gender'],
                    'Services': ['InternetService','OnlineSecurity','OnlineBackup'],
                    'Charges': ['MonthlyCharges','TotalCharges']
                    }
    dct_relations = {'ORG': ['Customer', 'Demographics'],
                     'PWR': ['Customer', 'Services'],
                     'ENG': ['Customer', 'Charges'],
                     }

    features_classification = []

    return df, dct_entities, dct_relations, features_classification, target
# ----------------------------------------------------------------------------------------------------------------------
def prepare_dataset_railways():
    df = pd.read_csv(folder_in + 'railways.csv')
    return
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
def export_to_neo4j_trains():
    df, dct_entities, dct_relations, features, target = prepare_dataset_automotive()
    NEO4J.export_df_to_neo4j(df, dct_entities, dct_relations, drop_if_exists=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
def export_to_neo4j_telecom():
    df, dct_entities, dct_relations, features, target = prepare_dataset_telecom()
    NEO4J.export_df_to_neo4j(df, dct_entities, dct_relations, drop_if_exists=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
#export_toneo4j_hotels()
#export_to_neo4j_trains()
#export_to_neo4j_titanic()
#export_to_neo4j_telecom()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    export_to_neo4j_titanic()
    #llm_cnfg = llm_config.get_config_azure()

    # llm_cnfg = llm_config.get_config_openAI()
    # kg_config = llm_config.get_config_neo4j()
    # LLM = llm_models.get_model(llm_cnfg.filename_config_emb_model)
    #
    # query = "How many survived males from Southampton?"
    #query = "how many woman aged 50+ from Southampton has survived"
    # A = llm_chains.wrap_chain(llm_chains.get_chain_Neo4j(LLM, filename_config_neo4j))
    # llm_interaction.interaction_offline(A,query)
    NEO4J.close()
