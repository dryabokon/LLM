import pandas as pd
import tools_Azure_NLP
# ----------------------------------------------------------------------------------------------------------------------
filename_in = './data/ex_LLM/Godfather.txt'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
A = tools_Azure_NLP.Client_NLP('./secrets/private_config_azure_NLP.yaml')
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #df = A.entity_recognition_example(["I had a great trip to NY last week"])
    text = open(filename_in, 'r').read()
    entities = A.get_entities(text,categories=['Person'],min_confidence=0.9)
    # print(entities)

    A.analyze_actions(text)
