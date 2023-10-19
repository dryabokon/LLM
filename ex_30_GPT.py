import os
import yaml
from langchain.schema import HumanMessage
#from litellm import completion
# ----------------------------------------------------------------------------------------------------------------------
import tools_LLM_Azure
import tools_LLM_OPENAI
# ----------------------------------------------------------------------------------------------------------------------
def ex1(prompt):
    tools_LLM_OPENAI.LLM('./secrets/private_config_openai.yaml')
    response = tools_LLM_OPENAI.gpt3_completion(prompt)
    print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex2(prompt):
    chatmode=False

    LLM = tools_LLM_Azure.LLM('./secrets/private_config_azure_chat.yaml',chatmode=chatmode)
    if chatmode:
        prompt = [HumanMessage(content=prompt)]

    response = LLM(prompt)
    if chatmode:
        print(response.content)
    else:
        print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex3(prompt):
    with open('./secrets/private_config_azure_chat.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        os.environ["AZURE_API_KEY"] = config['azure']['openai_api_key']
        os.environ["AZURE_API_BASE"] = config['azure']['openai_api_base']
        os.environ["AZURE_API_VERSION"] = str(config['azure']['openai_api_version'])

    messages = [{"content": prompt, "role": "user"}]
    your_deployment_id = config['azure']['deployment_name']
    response = completion(f"azure/{your_deployment_id}", messages)
    response = response["choices"][0]["message"]["content"]
    print(response)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #prompt = 'Who framed Roger rabit?'
    with open('./data/ex_LLM/prompt2.txt', 'r') as f:
        prompt = f.read()

    #ex1(prompt)
    ex2(prompt)
    #ex3(prompt)



