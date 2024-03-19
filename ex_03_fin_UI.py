import re
import json
import os.path

import pandas as pd
from dash import Dash,html,Input, Output, callback_context
import dash_bootstrap_components as dbc
import uuid
# ---------------------------------------------------------------------------------------------------------------------
#import tools_Langchain
import tools_plotly
import tools_plotly_draw
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
U = tools_plotly_draw.DashDraw()
# ----------------------------------------------------------------------------------------------------------------------
def get_config_azure():
    filename_config_chat_model = './secrets/private_config_azure_chat.yaml'
    filename_config_emb_model = './secrets/private_config_azure_embeddings.yaml'
    filename_config_vectorstore = './secrets/private_config_azure_search.yaml'

    dct_config = {'engine': 'azure', 'chat_model': filename_config_chat_model,'emb_model': filename_config_emb_model, 'vectorstore': filename_config_vectorstore,'search_mode_hybrid':True}
    return dct_config
# ----------------------------------------------------------------------------------------------------------------------
dct_config_agent = get_config_azure()
dct_book = {'filename_in': './data/ex_LLM/MBA_Fin/AVG-ANNUAL-REPORT-2022-web.pdf', 'text_key': 'Godfather','azure_search_index_name': 'index-australian-wine-annual-report', 'search_field': 'token', 'select':'text'}
#A = tools_Langchain.Assistant(dct_config_agent['chat_model'], dct_config_agent['emb_model'],dct_config_agent['vectorstore'], chain_type='QA',search_mode_hybrid=dct_config_agent['search_mode_hybrid'])
#A.init_search_index(azure_search_index_name=dct_book['azure_search_index_name'],search_field=dct_book['search_field'], text_key=dct_book['select'])
# ----------------------------------------------------------------------------------------------------------------------
class Plotly_App:
    def __init__(self,folder_out,dark_mode=False):
        self.url_base_pathname = '/'
        self.folder_out = folder_out
        self.dark_mode = dark_mode
        self.filename_assets = folder_out+'./assets.json'
        self.PB = tools_plotly.Plotly_builder(dark_mode=self.dark_mode)
        self.first_callback_fired = False

        self.define_assets()
        self.import_assets()
        self.define_colors()
        self.app = Dash(external_stylesheets=([dbc.themes.FLATLY]), url_base_pathname=self.url_base_pathname)
        return
# ---------------------------------------------------------------------------------------------------------------------
    def define_assets(self):
        self.metrics_statements = ['Gross Profit', 'Revenue', 'Net Profit', 'Total Current Assets', 'Total Current Liabilities','Net debt: total borrowings less cash and cash equivalents','Total Equity','Cash and cash equivalents','Trade and other receivables']
        self.metrics_ratios = ['Gross Profit Margin', 'Net profit margin', 'EBITDAS  margin', 'ROC','Current Ratio', 'Quick ratio', 'Debt-to-equity ratio', 'Debt-to-EBITDA ratio']


        self.dct_title = {'id':'0','prompt_id':uuid.uuid4().hex,'prompt':'Prompt','prompt_readonly':False,
                                'response_id':uuid.uuid4().hex,'response':'Response',
                                'dep_id':uuid.uuid4().hex,'dep':'',
                                'post_proc_id':uuid.uuid4().hex,'post_proc':''}

        self.dct_intro = {'id': '1', 'prompt_id': uuid.uuid4().hex, 'prompt': 'Prompt','prompt_readonly':False,
                          'response_id': uuid.uuid4().hex, 'response': 'Response',
                          'dep_id': uuid.uuid4().hex, 'dep': '',
                          'post_proc_id': uuid.uuid4().hex, 'post_proc': ''}


        self.dct_metrics_statement_prev = {'id': '2', 'prompt_id': uuid.uuid4().hex, 'prompt': 'statements_prev_year','prompt_readonly':True,
                          'response_id': uuid.uuid4().hex, 'response': 'Response',
                          'dep_id': uuid.uuid4().hex, 'dep': '',
                          'post_proc_id': uuid.uuid4().hex, 'post_proc': ''}

        self.dct_metrics_statement_curr = {'id': '3', 'prompt_id': uuid.uuid4().hex, 'prompt': 'statements_curr_year',
                                           'prompt_readonly': True,
                                           'response_id': uuid.uuid4().hex, 'response': 'Response',
                                           'dep_id': uuid.uuid4().hex, 'dep': '',
                                           'post_proc_id': uuid.uuid4().hex, 'post_proc': ''}

        self.dct_metrics_ratios = {'id': '4', 'prompt_id': uuid.uuid4().hex, 'prompt': 'metrics_ratios',
                                   'prompt_readonly': True,
                                   'response_id': uuid.uuid4().hex, 'response': 'Response',
                                   'dep_id': uuid.uuid4().hex, 'dep': '',
                                   'post_proc_id': uuid.uuid4().hex, 'post_proc': 'Post processing'}

        self.list_of_dict = [self.dct_title,self.dct_intro,self.dct_metrics_statement_prev,self.dct_metrics_statement_curr,self.dct_metrics_ratios]
        return
# ---------------------------------------------------------------------------------------------------------------------
    def export_assets(self):

        with open(self.filename_assets, "w") as f:
            f.write('[\n')
            f.write(','.join([json.dumps(dct, indent=4) for dct in self.list_of_dict]))
            f.write('\n]')
        return
# ---------------------------------------------------------------------------------------------------------------------
    def import_assets(self):
        if os.path.isfile(self.filename_assets):
            with open(self.filename_assets, "r") as f:
                list_of_dict = json.loads(f.read())

            for i,dct in enumerate(list_of_dict):
                for k in ['prompt','response','dep','post_proc']:
                    self.list_of_dict[i][k] = dct[k]

        return
# ---------------------------------------------------------------------------------------------------------------------
    def define_colors(self):

        control_panel_dark = False

        self.clr_header = "#404040"
        self.clr_control = "#2b2b2b" if control_panel_dark else "#EEEEEE"
        self.clr_header_pressed = "#606060"
        self.clr_control_pressed = "#2b2b2b" if control_panel_dark else "#DDDDDD"
        self.clr_font_header = "#FFFFFF"
        self.clr_font_control    = "#FFFFFF" if control_panel_dark else "#000000"

        self.PB.turn_light_mode(dark_mode=control_panel_dark)
        self.color_curret_active = '#AAAAAA' if control_panel_dark else '#606060'
        self.color_curret = 'rgba(80, 80, 80, 0.60)' if control_panel_dark else 'rgba(205, 205, 205, 0.60)'

        self.style_header = {'font-size': '18px', 'height': '32px', 'background-color': '#404040', 'color': '#FFFFFF'}
        self.style_button_header  = {'background-color': self.clr_header , 'color': self.clr_font_header, 'font-size': 'x-small'}
        self.style_button_header_pressed  = {'background-color': self.clr_header_pressed , 'color': self.clr_font_header , 'font-size': 'x-small'}

        return
# ---------------------------------------------------------------------------------------------------------------------
    def build_block(self,dct_block):

        res = dbc.Row([  dbc.Col(width=1,children=dbc.Label(dct_block['id'])),
                         dbc.Col(width=9,children=[ dbc.Row(dbc.Input(id=dct_block['prompt_id'],readonly=dct_block['prompt_readonly'],value=dct_block['prompt'],style=self.style_header)),
                                                    dbc.Row(dbc.Textarea(id=dct_block['response_id'],value=dct_block['response'],rows=6))]),

                         dbc.Col(width=2,children=[ dbc.Row(dbc.Input(id=dct_block['dep_id'], value=dct_block['dep'])),
                                                    dbc.Row(dbc.Input(id=dct_block['post_proc_id'],value=dct_block['post_proc']))])
                         ])

        return res
# ---------------------------------------------------------------------------------------------------------------------
    def build_layout(self):
        header = dbc.Row(html.Div([html.Img(src=self.get_asset_url()+'image5.png')],style={'display': 'flex','justify-content': 'center','align-items': 'center','background-color': '#086A6A'}))
        res= [header]
        for dct in self.list_of_dict:
            res+=[self.build_block(dct),html.Br()]

        layout = dbc.Container(res, style={'width': '100%','font-family':'Ubuntu Mono'}, fluid=True)

        return layout
# ---------------------------------------------------------------------------------------------------------------------
    def get_asset_url(self):
        return './assets/'
# ---------------------------------------------------------------------------------------------------------------------
    def run_server(self,port):
        self.app.layout = self.build_layout()
        self.set_callbacks()
        self.app.run_server(port=port,debug=False, dev_tools_hot_reload = False)
        return
# ---------------------------------------------------------------------------------------------------------------------
    def are_refreshes_needed(self, prop_id):
        refresh_needed = False
        if self.dct_title['prompt_id'] in prop_id:
            refresh_needed = True

        return refresh_needed
# ---------------------------------------------------------------------------------------------------------------------
    def get_callback_payload_out(self,list_of_dicts):
        payload_out = [Output(dct['response_id'], 'value') for dct in list_of_dicts]
        return payload_out
# ---------------------------------------------------------------------------------------------------------------------
    def get_callback_payload_in(self,list_of_dicts):
        payload_in_prompts = [Input(dct['prompt_id'], 'value') for dct in list_of_dicts]
        payload_in_responses = [Input(dct['response_id'], 'value') for dct in list_of_dicts]
        payload_in_dep = [Input(dct['dep_id'], 'value') for dct in list_of_dicts]
        payload_in_post_proc = [Input(dct['post_proc_id'], 'value') for dct in list_of_dicts]
        return payload_in_prompts+payload_in_responses+payload_in_dep+payload_in_post_proc
# ---------------------------------------------------------------------------------------------------------------------
    def parse_ids(self,str_value):
        if str_value is None or len(str_value)==0:
            res = []
        else:
            res = [re.sub(r"[^0-9]", "", s) for s in str_value.split(',')]
            res = [int(r) for r in res if len(r)>0]
        return res
# ---------------------------------------------------------------------------------------------------------------------
    def evaluate_responses(self,response0,response1,response2,response3,response4,texts0,texts1,texts2,texts3,texts4):
        if response0[-1]!='~':response0 = A.Q(self.dct_title['prompt'],texts=texts0)
        if response1[-1]!='~':response1 = A.Q(self.dct_intro['prompt'],texts=texts1)

        maxcolwidths = 80
        q_post_proc = 'From the question (Q) and long answer (A) below, retrieve the answer as named entity or return N/A otherwise.'

        if len(response2)==0 or response2[-1] != '~':
            df = pd.DataFrame({'Data from report': self.metrics_statements,
                                          'last_year': [A.Q(f'Evaluate {m} from last year.', q_post_proc=q_post_proc,texts=texts2) for m in self.metrics_statements]})
            response2 = tools_DF.prettify(df, maxcolwidths=maxcolwidths, showindex=False)

        if len(response3)==0 or response3[-1] != '~':
            df = pd.DataFrame({'Data from report': self.metrics_statements,
                               'this_year': [A.Q(f'Evaluate {m} from this year.', q_post_proc=q_post_proc,texts=texts3) for m in self.metrics_statements]})
            response3 = tools_DF.prettify(df, maxcolwidths=maxcolwidths, showindex=False)

        if len(response4)==0 or response4[-1] != '~':
            df = pd.DataFrame({'Data from report': self.metrics_ratios,
                               'this_year': [A.Q(f'Evaluate {m} from this year.', q_post_proc=q_post_proc,texts=texts4) for m in self.metrics_ratios]})
            response4 = tools_DF.prettify(df, maxcolwidths=maxcolwidths, showindex=False)

        return response0,response1,response2,response3,response4
# ---------------------------------------------------------------------------------------------------------------------
    def set_callbacks(self):
        @self.app.callback(self.get_callback_payload_out([self.dct_title,self.dct_intro,self.dct_metrics_statement_prev,self.dct_metrics_statement_curr,self.dct_metrics_ratios]),
                           self.get_callback_payload_in ([self.dct_title,self.dct_intro,self.dct_metrics_statement_prev,self.dct_metrics_statement_curr,self.dct_metrics_ratios]))
        def global_callback(prompt0,prompt1,prompt2,prompt3,prompt4,response0,response1,response2,response3,response4,dep0,dep1,dep2,dep3,dep4,pp0,pp1,pp2,pp3,pp4):

            if any([self.list_of_dict[i]['prompt']!=x    for i,x in enumerate([prompt0,prompt1,prompt2,prompt3,prompt4])]) or \
               any([self.list_of_dict[i]['dep']   !=x    for i,x in enumerate([dep0,dep1,dep2,dep3,dep4])]) or \
               any([self.list_of_dict[i]['post_proc']!=x for i,x in enumerate([pp0,pp1,pp2,pp3,pp4])]):

                texts0 = [self.list_of_dict[i]['response'] for i in self.parse_ids(dep0)]
                texts1 = [self.list_of_dict[i]['response'] for i in self.parse_ids(dep1)]
                texts2 = [self.list_of_dict[i]['response'] for i in self.parse_ids(dep2)]
                texts3 = [self.list_of_dict[i]['response'] for i in self.parse_ids(dep3)]
                texts4 = [self.list_of_dict[i]['response'] for i in self.parse_ids(dep4)]
                response0,response1,response2,response3,response4 = self.evaluate_responses(response0,response1,response2,response3,response4,texts0,texts1,texts2,texts3,texts4)

            for i,prompt in enumerate([prompt0, prompt1, prompt2, prompt3, prompt4]):
                self.list_of_dict[i]['prompt']=prompt

            for i,response in enumerate([response0,response1,response2,response3,response4]):
                self.list_of_dict[i]['response']=response

            self.export_assets()

            return [response0, response1, response2, response3, response4]
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    dark_mode = False
    App = Plotly_App(folder_out=folder_out)
    App.run_server(port=8051)