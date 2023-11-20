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
from LLM import tools_Langchain
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
    #export_to_neo4j_trains()
    #export_to_neo4j_titanic()
    #export_to_neo4j_telecom()

    #dct_config_agent = get_config_neo4j()

    #query = "How many survived males from Southampton?"
    #query = "how many woman aged 50+ from Southampton has survived"
    #ex_completion_offline(query, dct_config_agent)

    #ex_completion_live(dct_config_agent)

    #NEO4J.close()
    lst = [['Acknowledgement',
            'Confirmation given by the driver to a request from the ETCS on-board that he/she has received information he/she needs to take into account.'],
           ['Applicable speed limit (in SR)',
            'The lowest speed limit of:\
            — maximum speed for SR,\
            — maximum train speed,\
            — timetable / Route Book,\
            — temporary speed restrictions (transmitted by other means than European Instruction 1, 2, 5, 6, 7 or 8),\
            — European Instruction.'],
           ['Authorisation for ERTMS train movement',
            'Permission for a train to move given by means of:\
            — a trackside signal at proceed aspect, or\
            — an MA, or\
            — a European Instruction:\
            — to start after preparing a movement, or\
            — to pass EOA, or\
            — to proceed after trip.'],

           ['Border crossing',
            'Location where trains cross from a railway network in one Member State to a railway network in another Member State.'],
           ['De-registration',
            'Termination of the temporary relationship between the telephone number and the train running number. This action can be initiated by the user of a GSM-R radio, by automatic systems or by the network authority. The de-registration allows the de-registered train running number to be re-used.'],
           ['Driver Machine Interface (DMI)',
            'Train device to enable communication between the ETCS on-board and the driver.'],
           ['Emergency propelling area', 'Area where propelling movements in RV are allowed.'],
           ['Emergency stop order',
            'ETCS order braking a train with the maximum brake force until the train is at a standstill.'],
           ['ETCS Location Marker',
            'Harmonised trackside ETCS marker board defined in EN 16494/2015(2)used to identify a potential EOA, e.g. the end of a block section.'],
           ['ETCS on-board', 'The part of ETCS installed on a railway vehicle.'],
           ['ETCS Stop Marker',
            'Harmonised trackside ETCS marker board defined in EN 16494/2015 used to:\
            — identify a potential EOA, and\
            —indicate the location where a driver has to stop the train, if running without an MA.'],
           ['ETCS operational train category',
            'Set of technical and/or operational characteristics of a train to which a specific ETCS speed profile applies.'],
           ['Functional number (GSM-R)',
            'Full number used within the functional addressing scheme to identify an end user or a system by function or role rather than by a specific item of radio equipment or user subscription.\
            The functional number can be divided into two parts:\
            — functional addressing (process of addressing a call using a specific number, representing the function a user is performing, rather than a number identifying the GSM-R on-board),\
            —location dependent addressing (process of addressing a particular function – typically a signaller – based on the current location of the user – typically a train).'],
           ['GSM-R mode',
            'Status of the GSM-R on-board which provides functions for:\
            — train movement,\
            — or movement of a shunting composition.'],
           ['GSM-R network', 'Radio network which provides GSM-R functions.'],
           ['GSM-R network marker',
            'Harmonised trackside GSM-R signal defined in EN 16494/2015 to indicate the network to be selected.'],
           ['GSM-R on-board', 'The part of GSM-R installed on a railway vehicle.'],
           ['Maximum speed for RV', 'Maximum speed given from the ETCS trackside in RV'],
           ['Maximum speed for SR', 'Maximum speed given from the ETCS trackside in SR.'],
           ['Movement Authority (MA)',
            'Permission for a train (shunting composition) to move to a specific location with supervision of speed.'],
           ['Non-stopping area',
            'Area defined by the Infrastructure Manager where it may not be safe or suitable to stop a train.'],
           ['Override EOA speed', 'Maximum speed when the override EOA function is active.'],
           ['Permitted speed',
            'Maximum speed at which a train can run without ETCS warning and/or brake intervention.'],
           ['Proceed aspect', 'Any signal aspect which permits the driver to pass the signal.'],
           ['Propelling', 'Movement of a train where the driver is not in the leading cab of the leading vehicle.'],
           ['Radio communication', 'Exchange of information between the ETCS on-board and the RBC/radio infill unit.'],
           ['Radio Block Centre (RBC)', 'ETCS trackside centralised unit controlling ETCS train movements in level 2.'],
           ['Radio hole',
            'A pre-defined area where it is not possible to establish a reliable radio communication channel.'],
           ['Registration', 'Temporary relationship between the telephone number and the train running number.'],
           ['Release speed', 'Maximum speed at which a train is allowed to reach the end of its MA.'],
           ['Revocation of MA', 'Withdrawal of a previous given Movement Authority.'],
           ['Route Book',
            'Description of the lines and the associated line-side equipment for the lines over which the driver will operate and relevant to the driving task.'],
           ['Securing', 'Measures to be applied to avoid unintentional movement of railway vehicles.'],
           ['Shunting movement', 'Way of moving vehicles without train data and controlled by shunting orders.'],
           ['Tandem',
            'Two or more traction units mechanically and pneumatically but not electrically coupled in the same train, each one requiring its own driver.'],
           ['Temporary speed restriction', 'Reduction of the line speed for a limited period of time.'],
           ['Text message', 'Information in writing displayed on the Driver Machine Interface.'],
           ['Train data', 'Information which describes the characteristics of a train.'],
           ['Train preparer', 'Staff in charge of the preparation of a train.'],
           ['Transition', 'Controlled change between the different ETCS levels.'],
           ['Transition point', 'Point where a transition between ETCS levels takes place.'],
           ['Trip',
            'Irrevocable application of the emergency brakes by ETCS until the train/shunting composition is at a standstill.']]
    pd.DataFrame(lst, columns=['Term', 'Definition']).to_csv('railways.csv', index=False)









