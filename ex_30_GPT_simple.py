import os
import yaml
from langchain.schema import HumanMessage
#from litellm import completion
# ----------------------------------------------------------------------------------------------------------------------
from LLM import tools_LLM_Azure
from LLM import tools_LLM_OPENAI
# ----------------------------------------------------------------------------------------------------------------------
def ex1(prompt):
    tools_LLM_OPENAI.LLM('./secrets/private_config_openai.yaml')
    response = tools_LLM_OPENAI.gpt3_completion(prompt)
    print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex2(prompt):
    chatmode=False

    #LLM = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat.yaml',chatmode=chatmode)
    LLM = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat_zs2.yaml',chatmode=chatmode)
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

    ex1(prompt)
    #ex3(prompt)





