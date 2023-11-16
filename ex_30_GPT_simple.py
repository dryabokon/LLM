import os
import yaml
from langchain.schema import HumanMessage
# ----------------------------------------------------------------------------------------------------------------------
from LLM import tools_LLM_OPENAI
from LLM import tools_LLM_Azure
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
def ex1(prompt):

    A = tools_LLM_OPENAI.Assistant_OPENAILLM('./secrets/private_config_openai.yaml',folder_out)
    response = A.Q(prompt)
    print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex2(prompt):
    chatmode=True

    LLM = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat.yaml',chatmode=chatmode)
    #LLM = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat_zs2.yaml',chatmode=chatmode)
    if chatmode:
        prompt = [HumanMessage(content=prompt)]

    response = LLM(prompt)

    if chatmode:
        print(response.content)
    else:
        print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    prompt = 'Who framed Roger rabit?'

    #ex1(prompt)
    ex2(prompt)