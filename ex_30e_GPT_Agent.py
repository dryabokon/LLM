from langchain.prompts import PromptTemplate
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
from LLM import tools_Langchain_Agent
from langchain.chains import LLMChain
from langchain_experimental import pal_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
# ----------------------------------------------------------------------------------------------------------------------
def get_config():

    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'
    # filename_config_chat_model = './secrets/private_config_openai.yaml'
    # filename_config_emb_model = './secrets/private_config_openai.yaml'
    # filename_config_vectorstore = './secrets/private_config_pinecone.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model,'vectorstore': filename_config_vectorstore}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
def ex_API():
    #q = "6+8=?"
    # q = "Shirt options for men in blue color."
    # res = A.Q(q)
    # print(q)
    # print(res)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_template():
    prompt = PromptTemplate(input_variables=["product"],template="What is a good name for a company that makes {product}?")
    print(prompt.format(product="podcast player"))

    llmchain = LLMChain(llm=A.LLM, prompt=prompt)
    res = llmchain.run("podcast player")
    print(res)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dct_config_agent = get_config()
    A = tools_Langchain_Agent.Agent(dct_config_agent['chat_model'], chain_type='QA')

    palchain = pal_chain.PALChain(llm=A.LLM)
    res = palchain.run("If my age is half of my dad's age and he is going to be 60 next year, what is my current age?")
    print(res)

    # qa_chain = load_qa_chain(llm=A.LLM, input_documents=[],verbose=True)
    # res = qa_chain.run("If my age is half of my dad's age and he is going to be 60 next year, what is my current age?")
    # print(res)

    # tools = load_tools(["pal-math"], llm=A.LLM)
    # agent = initialize_agent(tools,A.LLM,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
    # agent.run("If my age is half of my dad's age and he is going to be 60 next year, what is my current age?")









