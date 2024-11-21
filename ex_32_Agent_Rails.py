import os.path
import os.path
import cv2
import numpy
import pandas as pd
import warnings
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas_gbq
warnings.filterwarnings( 'ignore', module = 'langchain' )
from tqdm import tqdm
from google.cloud import bigquery
# ----------------------------------------------------------------------------------------------------------------------
import tools_image
import tools_draw_numpy
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_config,llm_Agent_BQ,llm_interaction
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
def time_to_seconds(time_str):
    if len(time_str) == 0:return None
    h = int(time_str[:2])
    m = int(time_str[2:4])
    if len(time_str)>4:
        s = time_str[4:].replace('½', '.5').replace('¼', '.25').replace('¾', '.75')
    else:
        s=0
    return 60*60*h + m*60 + int(60*float(s))
# ----------------------------------------------------------------------------------------------------------------------
def scrap_timetable(filename_out):
    res = requests.get('https://www.realtimetrains.co.uk/search/detailed/gb-nr:MIA/2024-06-18/0000-2359?stp=WVSC&show=all&order=wtt')
    with open(filename_out, 'w', encoding='utf-8') as file:
        file.write(res.text)
    return
# ----------------------------------------------------------------------------------------------------------------------
def parse_timetable(filename_html_in):
    location = 'Manchester Airport'

    with open(filename_html_in, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    services = soup.find_all('a', class_='service')
    parsed_services = []
    for service in services:
        service_data = {
            "tid": service.find('div', class_='tid').text if service.find('div', class_='tid') else "",
            "arr_fact": service.find('div', class_='time real a act c rt').text if service.find('div',class_='time real a act c rt') else "",
            "arr_plan": service.find('div', class_='time plan a gbtt').text if service.find('div',class_='time plan a gbtt') else "",
            "arr_plan_wtt": service.find('div', class_='time plan d wtt').text if service.find('div',class_='time plan d wtt') else "",
            "location_d_ts": service.find('div', class_='location d ts').text if service.find('div',class_='location d ts') else "",
            "location_d": service.find('div', class_='location d').text if service.find('div',class_='location d') else "",
            "location_o_ts": service.find('div', class_='location o ts').text if service.find('div',class_='location o ts') else "",
            "location_o": service.find('div', class_='location o').text if service.find('div',class_='location o') else "",
            "dep_plan": service.find('div', class_='time plan d wtt').text.strip() if service.find('div',class_='time plan d wtt') else "",
            "dep_plan_gbtt": service.find('div', class_='time plan d gbtt').text.strip() if service.find('div',class_='time plan d gbtt') else "",
            "dep_plan_ts": service.find('div', class_='time plan d wtt ts').text.strip() if service.find('div',class_='time plan d wtt ts') else "",
            "dep_fact": service.find('div', class_='time real d exp').text.strip() if service.find('div',class_='time real d exp') else "",
            "dep_fact2": service.find('div', class_='time real d act c rt').text.strip() if service.find('div',class_='time real d act c rt') else "",
            "stp": service.find('div', class_='stp').text if service.find('div', class_='stp') else "",
            "toc": service.find('div', class_='toc').text if service.find('div', class_='toc') else "",
            "pl_act": service.find('div', class_='platform c act').text if service.find('div',class_='platform c act') else "",
            "pl_exp": service.find('div', class_='platform c exp').text if service.find('div',class_='platform c exp') else "",
        }
        parsed_services.append(service_data)

    df = pd.DataFrame(parsed_services)
    df['location_o'] = df['location_o'].apply(lambda x: x if len(x)>0 else location)
    df['location_d'] = df['location_d'].apply(lambda x: x if len(x)>0 else location)

    df.loc[df['arr_plan'] == '', 'arr_plan'] = df.loc[df['arr_plan'] == '', 'arr_plan_wtt']
    df.loc[df['dep_plan'] == '', 'dep_plan'] = df.loc[df['dep_plan'] == '', 'dep_plan_ts']
    df.loc[df['dep_plan'] == '', 'dep_plan'] = df.loc[df['dep_plan'] == '', 'dep_plan_gbtt']
    df.loc[df['dep_fact'] == '', 'dep_fact'] = df.loc[df['dep_fact'] == '', 'dep_fact2']

    df['delta_arr'] = df['arr_fact'].apply(time_to_seconds) - df['arr_plan'].apply(time_to_seconds)
    df['delta_dep'] = df['dep_fact'].apply(time_to_seconds) - df['dep_plan'].apply(time_to_seconds)

    df['delta_dep'] = df['delta_dep'].apply(lambda x: x if abs(x) < 86400-1000 else x-86400*numpy.sign(x))
    df['delta_arr'] = df['delta_arr'].apply(lambda x: x if abs(x) < 86400-1000 else x-86400*numpy.sign(x))

    df = df[['tid','arr_plan','arr_fact','location_o','location_d','dep_plan','dep_fact','stp','toc','pl_act','pl_exp','delta_arr','delta_dep']]
    return df
# ----------------------------------------------------------------------------------------------------------------------
def scrap_map_data(filename_out):

    URL = 'https://raildar.co.uk/map/MIA'
    driver_path = 'C:/Users/acer/.wdm/drivers/chromedriver/win64/125.0.6422.141/chromedriver-win32/chromedriver.exe'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    time.sleep(5)
    with open(filename_out, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    driver.quit()
    return
# ----------------------------------------------------------------------------------------------------------------------
def build_map_image(filename_html_in, scale_factor=2.5):
    with open(filename_html_in, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tiles = soup.find_all(class_='tile')
    parsed_tiles = []

    for tile in tiles:
        style = tile.get('style')
        if style:
            style_dict = dict(item.split(":") for item in style.split(";") if item)
            image_id = tile.find('img').get('src').split('/')[-1]
            width = float(style_dict.get('width', '').strip().replace('px', ''))
            height = float(style_dict.get(' height', '').strip().replace('px', ''))
            left = float(style_dict.get(' left', '').strip().replace('px', ''))
            top = float(style_dict.get(' top', '').strip().replace('px', ''))
            parsed_tiles.append({'image_id':image_id,'left': left, 'top': top, 'width': width, 'height': height})

    df = pd.DataFrame(parsed_tiles)

    W,H = int(scale_factor*df['width'].max()),int(scale_factor*df['height'].max())
    image_large = numpy.full((int(scale_factor*df['top'].max() + H), int(scale_factor*df['left'].max() + W), 3), 255, dtype=numpy.uint8)
    for r in range(df.shape[0]):
        filename = './data/ex_images/06/' + df.loc[r, 'image_id']
        image = cv2.imread(filename) if os.path.isfile(filename) else numpy.full((H, W, 3), 255, dtype=numpy.uint8)
        image_small = tools_image.smart_resize(image, int(H), int(W))
        image_large = tools_image.put_image(image_large, image_small, int(scale_factor*df.loc[r, 'top']), int(scale_factor*df.loc[r, 'left']))

    #print(tools_DF.prettify(df,showindex=False))

    return image_large
# ----------------------------------------------------------------------------------------------------------------------
def draw_trains_on_map(filename_html_in,df_trains=None,scale_factor=2.5):
    image = build_map_image(filename_html_in,scale_factor=scale_factor)
    image = tools_image.desaturate(image,level=0.8)

    with open(filename_html_in, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    trains = soup.find_all(class_='headcode')
    parsed_trains = []
    for train in trains:
        train_id = train.string

        style_parent = train.parent.parent.parent.parent.parent.parent.get('style')
        style = train.parent.parent.get('style')

        if style_parent and style:
            style_dict = dict(item.split(":") for item in style_parent.split(";") if item)
            left_parent = float(style_dict.get(' left', '').strip().replace('px', ''))
            top_parent = float(style_dict.get(' top', '').strip().replace('px', ''))

            style_dict = dict(item.split(":") for item in style.split(";") if item)
            left = float(style_dict.get('left', '').strip().replace('px', ''))+left_parent
            top = float(style_dict.get(' top', '').strip().replace('px', ''))+top_parent
            parsed_trains.append([train_id, left, top])
            image = tools_draw_numpy.draw_text(image, train_id, (scale_factor*left     , scale_factor*top), (0, 212, 250), (32, 32, 32), font_size=16,vert_align='center')
            df_local = df_trains[df_trains['tid'] == train_id][['location_o','location_d','delta_arr','delta_dep']]
            if not df_local.empty:
                df_local = df_local.iloc[0]
                label = df_local['location_o'] + ' -> ' + df_local['location_d']
                if not pd.isna(df_local['delta_arr']):
                    label+= ' arr ' + '%+d'%int(df_local['delta_arr']) + ' sec'
                if not pd.isna(df_local['delta_dep']):
                    label+= ' dep ' + '%+d'%int(df_local['delta_dep']) + ' sec'

                image = tools_draw_numpy.draw_text(image, label, (scale_factor*left + 50, scale_factor*top), (0, 212, 250),(32, 32, 32), font_size=16,vert_align='center')


    #df = pd.DataFrame(parsed_trains)
    #print(tools_DF.prettify(df,showindex=False))

    return image
# ----------------------------------------------------------------------------------------------------------------------
def ex_import():
    filename_timetable_html = folder_out + 'MIA_timetable.html'
    filename_map_html = folder_out + 'MIA_map.html'

    scrap_map_data(filename_map_html)
    scrap_timetable(filename_timetable_html)
    df_trains = parse_timetable(filename_timetable_html)
    df_trains.to_csv(folder_out+'MIA_timetable.csv', index=False)
    #pandas_gbq.to_gbq(df_trains, 'ml-ops-poc-695.trains2.trains_table', project_id=Vector_Searcher_VertexAI.config['GCP']['PROJECT_ID'])

    image = draw_trains_on_map(filename_map_html,df_trains,scale_factor=1.5)
    cv2.imwrite(folder_out+'MIA.png', image)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_import2():

    pl = ['WAT','VIC','LST','LBG','KGX','EUS','CLJ','GLC','MAN','BHM','PAD','EDB','LDS','CHX','STP','FST','LIV','RDG','BRI','YRK']

    df = pd.DataFrame()

    for p in tqdm(pl,total=len(pl)):
        filename_temp = folder_out + f'delme{p}'
        res = requests.get(f'https://www.realtimetrains.co.uk/search/detailed/gb-nr:{p}/2024-06-17/0000-2359?show=all')
        with open(filename_temp+'.html', 'w', encoding='utf-8') as file:
            file.write(res.text)
            df_trains = parse_timetable(filename_temp+'.html')
            df_trains.to_csv(filename_temp+'.csv', index=False)
            df = pd.concat([df,df_trains])
        #os.remove(filename_temp+'.html')

    df.to_csv(folder_out+'timetable_top20.csv', index=False)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_import_to_BQ():

    project, dataset, table_name = 'ml-ops-poc-695', 'trains2', 'trains_table'

    client = bigquery.Client(project=project)
    query = f"""DELETE FROM `{project}.{dataset}.{table_name}` WHERE TRUE """
    query_job = client.query(query)
    query_job.result()

    df_trains = pd.read_csv(folder_out + 'timetable_top20.csv')
    pandas_gbq.to_gbq(df_trains, f'{project}.{dataset}.{table_name}', project_id=project)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_offline():

    project,dataset,table_name = 'ml-ops-poc-695','trains2','trains_table'
    A = llm_Agent_BQ.Agent_BQ(project, dataset, table_name)

    q1 = 'Count # of records'
    q2 = 'give me top 5 late arriving trains'
    q3 = 'late departing'

    llm_interaction.interaction_offline(A, [q1,q2,q3], do_debug=True, do_spinner=True)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_offline2():

    project,dataset,table_name = 'ml-ops-poc-695','trains2','conditions'
    A = llm_Agent_BQ.Agent_BQ(project, dataset, table_name)

    q1 = 'Count # of records'
    q2 = 'give me unique units'

    llm_interaction.interaction_offline(A, [q1,q2], do_debug=True, do_spinner=True)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_live():

    project,dataset,table_name = 'ml-ops-poc-695','trains2','trains_table'
    A = llm_Agent_BQ.Agent_BQ(project, dataset, table_name)
    llm_interaction.interaction_live(A, do_debug=True,do_spinner=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #ex_agent_offline()
    ex_agent_offline2()
    #ex_agent_live()
    #ex_import2()
    #ex_import_to_BQ()

