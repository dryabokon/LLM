import streamlit as st
# ----------------------------------------------------------------------------------------------------------------------
import sys
sys.path.append('../tools/')
sys.path.append('../tools/LLM2/')
from LLM2 import llm_config,llm_models,llm_chains,llm_RAG,llm_interaction
import tools_Azure_Search
import tools_time_profiler
# ---------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
TP = tools_time_profiler.Time_Profiler()
# ---------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0;
                    padding-bottom: 0;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }

                header {visibility: hidden;}

        </style>
        """, unsafe_allow_html=True)
# ---------------------------------------------------------------------------------------------------------------------
def streamlit_UI(A,do_spinner=True,do_debug=True):
    st.title("Gen AI | Demo chat bot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "What is your question?"}]

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if query := st.chat_input(key='chat'):
        st.chat_input(key='quiet', disabled=True)
        user_prompt = {"role": "user", "content": query}
        st.session_state.chat_history.append(user_prompt)
        with st.chat_message('user'):
            st.markdown(query)

        with st.chat_message('assistant'):
            #msg,_ = A.run_query(query)
            msg,_ = llm_interaction.interaction_offline(A, query, do_debug=True, do_spinner=True)

        st.session_state.chat_history.append({"role": "assistant", "content": msg})
        st.chat_input(disabled=False)
        st.rerun()

    return
# ---------------------------------------------------------------------------------------------------------------------
dct_book1_godfather = {'filename_in': './data/ex_LLM/Godfather_2.txt', 'azure_search_index_name': 'idxgfvect2', 'search_field': 'token', 'select': 'text'}
dct_book8_StackOverflow = {'azure_search_index_name':'stackoverflow125body','search_field': 'token', 'select': 'answer_body'}
queries8 = ['How to create a bar chart with gradient colours?','How to plot stacked bar if number of columns is not known?','how to save seaborn chart to disk?','how to limit the range of X axis?'][:1]
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # df_finance = pd.read_csv('./data/output/Book1.csv')
    # df_automotive = pd.read_csv('./data/ex_datasets/Automobile_data.csv')
    # df_churn = pd.read_csv('./data/ex_datasets/dataset_churn.csv')

    #llm_cnfg = llm_config.get_config_openAI()
    llm_cnfg = llm_config.get_config_azure()

    # LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    # tools = llm_tools.get_tools_pandas_v02(df_finance)
    # A = llm_Agent.Agent(LLM, tools, verbose=True)

    LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
    chain = llm_chains.get_chain_chat(LLM)
    #dct_book = dct_book1_godfather
    dct_book = dct_book8_StackOverflow

    Vector_Searcher_Azure = tools_Azure_Search.Client_Search('./secrets/GL/private_config_azure_search.yaml',index_name=dct_book['azure_search_index_name'])
    A = llm_RAG.RAG(chain, Vector_Searcher_Azure)

    A.select = dct_book['select']
    #streamlit_UI(A)
    llm_interaction.interaction_offline(A, queries8, do_debug=True, do_spinner=False)

