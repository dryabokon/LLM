# http://gl-test-rag.canadaeast.cloudapp.azure.com:8050/
import time
import json
import pandas as pd
import dash
from dash import Dash, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import sys
from dash import dcc
# ----------------------------------------------------------------------------------------------------------------------
sys.path.insert(1, './tools/')
from LLM2 import llm_config, llm_models, llm_tools, llm_chains, llm_Agent
# ---------------------------------------------------------------------------------------------------------------------
import tools_plotly

# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'


# ----------------------------------------------------------------------------------------------------------------------
class Plotly_App:
    def __init__(self, folder_out, df, dark_mode=False):
        self.url_base_pathname = '/'
        self.folder_out = folder_out
        self.dark_mode = dark_mode
        self.filename_assets = folder_out + './assets.json'
        self.PB = tools_plotly.Plotly_builder(dark_mode=self.dark_mode)
        self.first_callback_fired = False

        self.define_colors()
        self.setup_agent(df)
        self.app = Dash(external_stylesheets=([dbc.themes.FLATLY]), url_base_pathname=self.url_base_pathname)
        return

    # ---------------------------------------------------------------------------------------------------------------------
    def setup_agent(self, df):
        llm_cnfg = llm_config.get_config_openAI()
        # llm_cnfg = llm_config.get_config_azure()
        LLM = llm_models.get_model(llm_cnfg.filename_config_chat_model, model_type='QA')
        tools = llm_tools.get_tools_pandas_v01(df)
        tools.extend(llm_tools.get_tool_IRR())
        tools.extend(llm_tools.get_tool_sale_for_target_IRR())
        self.A = llm_Agent.Agent(LLM, tools, verbose=True)
        return

    # ---------------------------------------------------------------------------------------------------------------------
    def define_colors(self):
        control_panel_dark = False

        self.clr_header = "#404040"
        self.clr_control = "#2b2b2b" if control_panel_dark else "#EEEEEE"
        self.clr_header_pressed = "#606060"
        self.clr_control_pressed = "#2b2b2b" if control_panel_dark else "#DDDDDD"
        self.clr_font_header = "#FFFFFF"
        self.clr_font_control = "#FFFFFF" if control_panel_dark else "#000000"

        self.PB.turn_light_mode(dark_mode=control_panel_dark)
        self.color_curret_active = '#AAAAAA' if control_panel_dark else '#606060'
        self.color_curret = 'rgba(80, 80, 80, 0.60)' if control_panel_dark else 'rgba(205, 205, 205, 0.60)'

        self.style_header = {'font-size': '18px', 'height': '32px', 'background-color': '#404040', 'color': '#FFFFFF'}
        self.style_button = {'background-color': '#389394', 'color': self.clr_font_header, 'font-size': 'large'}
        # self.style_button_header_pressed  = {'background-color': self.clr_header_pressed , 'color': self.clr_font_header , 'font-size': 'x-small'}

        return

    # ---------------------------------------------------------------------------------------------------------------------
    def build_layout(self):
        # header = dbc.Row(html.Div([html.Img(src=self.get_asset_url() + 'image6.png')],
        #                           style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
        #                                  'background-color': '#E4E4E4'}))
        # output = dbc.Row(dbc.Textarea(id='output', value=''))
        # input = dbc.Row(dbc.Input(id='input', value=''))
        # button = dbc.Row(dbc.Button("Run", id='submit', color="", size="sm", style=self.style_button))
        #
        # res = [header, output, input, button]
        # layout = dbc.Container(res, style={'width': '50%', 'font-family': 'Ubuntu Mono'}, fluid=True)

        layout = html.Div([
            html.Div([
                html.Label("Enter text:"),
                dcc.Input(id="input-text", type="text", style={"margin-right": "10px"}),
                html.Button("Submit", id="submit-button")
            ]),
            html.Div(id="progress-output", style={"margin-top": "20px"}),
            html.Div(id="final-output", style={"margin-top": "20px"})
        ])

        return layout

    # ---------------------------------------------------------------------------------------------------------------------
    def get_asset_url(self):
        return './assets/'

    # ---------------------------------------------------------------------------------------------------------------------
    def run_server(self, port):
        self.app.layout = self.build_layout()
        self.set_callbacks()
        self.app.run_server(port=port, debug=False, dev_tools_hot_reload=False)
        return

    # ---------------------------------------------------------------------------------------------------------------------
    def is_refresh_needed(self, prop_id):
        refresh_needed = False
        if 'submit' in prop_id:
            refresh_needed = True

        return refresh_needed

    # ---------------------------------------------------------------------------------------------------------------------
    # def set_callbacks(self):
    #     @self.app.long_callback(output=
    #                             [
    #                                 Output('output', 'value')
    #                             ],
    #                             imput=
    #                             [
    #                                 Input('output', 'value'),
    #                                 Input('input', 'value'),
    #                                 Input('submit', 'n_clicks')
    #                             ],
    #                             running=
    #                             [
    #                                 (Output('output', 'value'), True, False)
    #                              ])
    #     def global_callback(txt_output, txt_input, btn_click):
    #         ctx = dash.callback_context
    #         refresh_needed = self.is_refresh_needed(ctx.triggered[0]['prop_id'])
    #         response = txt_output
    #         if refresh_needed:
    #             prompt = txt_input
    #             # response = self.A.run_query(prompt)
    #             response = prompt
    #             for step in range(10):
    #                 time.sleep(10)
    #                 return f"Long process finished for '{step}'!", ""
    #
    #         return [response]

    def set_callbacks(self):
        @self.app.long_callback(
            output=[
                dash.Output("final-output", "children"),
                dash.Output("progress-output", "children"),
            ],
            inputs=[
                dash.Input("submit-button", "n_clicks"),
                dash.State("input-text", "value")
            ],
            running=[
                (dash.Output("submit-button", "disabled"), True, False),
                (dash.Output("input-text", "disabled"), True, False)
            ],
            progress=dash.Output("progress-output", "children"),
            prevent_initial_call=True
        )
        def update_output(set_progress, n_clicks, input_value):
            if n_clicks:
                total_steps = 10
                for step in range(total_steps):
                    time.sleep(1)  # Simulating a long process
                    set_progress(f"Processing '{input_value}'... {int((step + 1) / total_steps * 100)}%")
                return f"Long process finished for '{input_value}'!", ""
            return "", "Enter text and click submit to start."
# ---------------------------------------------------------------------------------------------------------------------
def prepare_dataset_hotels():
    dct = json.load(open('./data/ex_datasets/hotels.json'))
    fields = ['HotelId', 'HotelName', 'Description', 'Category', 'Rating', 'ParkingIncluded', 'Address']
    res = [[d[k] for k in fields] for d in dct['value']]
    df = pd.DataFrame(res, columns=fields)
    df['Address'] = df['Address'].apply(lambda x: x['City'])

    return df


# ---------------------------------------------------------------------------------------------------------------------
# what is common for hotels in NY
# according to historical dataset, what are the factors to segment/predict churn and retained customers ?
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # df = pd.read_csv('./data/ex_datasets/hotels2.csv')
    df = pd.read_csv('./data/ex_datasets/dataset_churn.csv')
    App = Plotly_App(folder_out=folder_out, df=df)
    App.run_server(port=8051)
