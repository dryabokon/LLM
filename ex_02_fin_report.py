import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
import tools_Langchain
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
dct_config_agent = get_config_azure()
dct_book1 = {'filename_in': './data/ex_LLM/MBA_Fin/AVG-ANNUAL-REPORT-2022-web.pdf'               , 'text_key': 'wine-AVG'       ,'azure_search_index_name': 'index-australian-wine-annual-report', 'search_field': 'token', 'select':'text'}
dct_book2 = {'filename_in': './data/ex_LLM/MBA_Fin/Purcari-Wineries-PLC-_-Annual-Report-2021.pdf', 'text_key': 'wine-purcari'   ,'azure_search_index_name': 'index-purcari-annual-report', 'search_field': 'token', 'select':'text'}
# ----------------------------------------------------------------------------------------------------------------------
dct_book = dct_book1
A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
A.init_search_index(azure_search_index_name=dct_book['azure_search_index_name'],search_field=dct_book['search_field'], text_key=dct_book['select'])
# ----------------------------------------------------------------------------------------------------------------------
def get_table(df):
    html_header = '\n'.join([f'<th scope="col">{col}</th>' for col in df.columns])

    html_body = ''
    for r in range(df.shape[0]):
        html_row = '\n'.join([f'<td>{value}</td>' for value in df.iloc[r, :]])
        html_body+=f'<tr>{html_row}</tr>\n'

    html_table = f'<table class="table table-bordered table-sm">\n\
                    <thead class="table-dark">\n' \
                 f'<tr>\n' \
                 f'{html_header}</tr>\n</thead>\
        <tbody>{html_body}</tbody>\
    </table>'

    return html_table
# ----------------------------------------------------------------------------------------------------------------------
metrics_ratios = ['Gross Profit','Revenue','Net Profit','Total Assets','Total Current Liabilities']
metrics_income_statement = ['Gross Profit Margin','Net profit margin','EBITDAS  margin','ROC']
metrics_balance_sheet = ['Net debt: total borrowings less cash and cash equivalents', 'Quick ratio', 'Debt-to-equity ratio', 'Debt-to-EBITDA ratio']
ratios_balance_sheet = ['Current Ratio','Quick ratio','Debt-to-equity ratio','Debt-to-EBITDA ratio']

# ----------------------------------------------------------------------------------------------------------------------
dtc_QA= {
    'xxx_company':A.Q('Provide company name reported in the financial report ? Just name, brief response, 2-3 words.'),
    'xxx_period':A.Q('What is the period of financial report? Brief response please !'),
    'xxx_introduction':A.Q('Write brief intro to financial report analysis to be made with respect to the annual financial report.'),

    'xxx_table_metrics_general':get_table(pd.DataFrame({'Metric':metrics_ratios,
                                                        'Description':[A.Q(f'Give description of {m} metric.',context_free=True) for m in metrics_ratios]})),

    'xxx_table_metrics_data_from_report':get_table(pd.DataFrame({'Data from report':metrics_ratios,
                                                                 'last_year':[A.Q(f'Evaluate {m} from last year') for m in metrics_ratios],
                                                                 'this_year':[A.Q(f'Evaluate {m} from this year') for m in metrics_ratios]})),

    'xxx_table_ratios_income_statement':get_table(pd.DataFrame({'Data from report':metrics_income_statement,
                                                                 'last_year':[A.Q(f'Evaluate {m} from last year') for m in metrics_income_statement],
                                                                 'this_year':[A.Q(f'Evaluate {m} from this year') for m in metrics_income_statement],
                                                                 })),
    'xxx_income_statement_analysis':A.Q(f'Provide company performance analysis based on %s.'%','.join(metrics_income_statement)),

    'xxx_table_metrics_balance_sheet_general':get_table(pd.DataFrame({'Metric':metrics_balance_sheet,'Description':[A.Q(f'Give description of {m}.',context_free=True) for m in metrics_balance_sheet]})),

    'xxx_table_reported_balance_sheet_metrics': get_table(pd.DataFrame({'Data from report':metrics_balance_sheet ,
                      'last_year': [A.Q(f'Evaluate {m} from last year') for m in metrics_balance_sheet],
                      'this_year': [A.Q(f'Evaluate {m} from this year') for m in metrics_balance_sheet]
                      })),

    'xxx_table_reported_balance_sheet_ratios': get_table(pd.DataFrame({'Data from report': ratios_balance_sheet,
                                                                'last_year': [A.Q(f'Evaluate {m} from last year',context_from_cache=True) for m in ratios_balance_sheet],
                                                                'this_year': [A.Q(f'Evaluate {m} from this year',context_from_cache=True) for m in ratios_balance_sheet]
                                                                })),

    'xxx_balance_sheet_analysis':A.Q('Provide Balance Sheet and Leverage Ratios analysis.'),
    'xxx_cashflow_statement_analysis':A.Q('Provide company performance analysis based on Cashflow.'),
    'xxx_profitability_analysis':A.Q('Provide company profitability analysis.'),
    'xxx_conclusion':A.Q('Provide conclusion about company performance based on finantial statements.')
}
# ----------------------------------------------------------------------------------------------------------------------
def compose_single_html(filename_out,dct_QA):

    html_str = open('./data/fin_report_02.html',mode='r').read()
    for k,v in dct_QA.items():
        html_str = html_str.replace(k, v)

    html_str = html_str.encode('ascii', 'ignore').decode('ascii')
    open(filename_out,mode='w').write(html_str)
    return
# ----------------------------------------------------------------------------------------------------------------------
def add_document_to_azure():
    A.add_document_azure(dct_book['filename_in'], azure_search_index_name=dct_book['azure_search_index_name'])
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #add_document_to_azure()
    compose_single_html(folder_out+'res.html',dtc_QA)
