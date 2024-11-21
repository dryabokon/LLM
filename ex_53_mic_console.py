import os

import pandas as pd
import cv2
import sys
import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel
from tqdm import tqdm
# ----------------------------------------------------------------------------------------------------------------------
sys.path.append('../tools/')
sys.path.append('../tools/LLM2/')
import tools_DF
import tools_VertexAI_Search
import tools_image
import tools_IO
# ----------------------------------------------------------------------------------------------------------------------
Vector_Searcher = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')
Vector_Searcher.table_name = 'AEK'
# ----------------------------------------------------------------------------------------------------------------------
def run_query(query,select,limit=6):

    df = Vector_Searcher.search_vector(query, select=select, as_df=True, limit=2*limit)
    if df.shape[0] == 0:return 'No results found',[]
    if df.shape[0] == 0: return 'No relevant results found',[]

    df = df.sort_values(by='score', ascending=True)[:limit]
    res_txt = tools_DF.prettify(df, showindex=False)
    images = [cv2.imread('./data/ex_images/AEK/profile_%04d.png'%i) for i in df['track_id'].values]
    images = [tools_image.smart_resize(im,target_image_height=320) if im is not None else None for im in images]

    return res_txt, images
# ----------------------------------------------------------------------------------------------------------------------
def import_data_text():
    df = pd.read_csv('./data/ex_datasets/df_LPs.csv')[['track_id', 'model_color', 'mmr_type', 'conf_mmr']]
    Vector_Searcher = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')
    Vector_Searcher.add_tabular_data('AEK',df,col_text=['model_color','mmr_type'],remove_table=True)
    return
# ----------------------------------------------------------------------------------------------------------------------
def import_data_im(folder_in):

    Vector_Searcher = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')

    #vertexai.init(project = Vector_Searcher.config['GCP']['PROJECT_ID'], location = Vector_Searcher.config['GCP']['REGION'])
    # model = ImageTextModel.from_pretrained("imagetext@001")
    # filenames = tools_IO.get_filenames(folder_in, '*.png')[152:]

    # mode = 'w'
    # filename_out = './data/output/captions.csv'
    # if os.path.isfile(filename_out):
    #     os.remove(filename_out)
    #
    # for filename in tqdm(filenames, total=len(filenames)):
    #     im = cv2.imread(folder_in + filename)
    #     if im.shape[0]*im.shape[1] < 32*32:
    #         caption = 'Image too small'
    #     else:
    #         try:
    #             caption = model.get_captions(Image.load_from_file(folder_in + filename))[0]
    #         except:
    #             caption = 'No caption'
    #     df_one = pd.DataFrame({'track_id': [int(filename.split('_')[1].split('.')[0]) ],'text': [caption]})
    #     df_one.to_csv(filename_out, mode=mode, index=False, header=(mode == 'w'))
    #     mode = 'a'

    df = pd.read_csv('./data/output/captions.csv')
    Vector_Searcher.add_tabular_data('AEK', df, col_text=['text'], remove_table=True)

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # res_text, images = run_query('green Toyota', select=['track_id', 'text', 'score'],limit=4)
    # print(res_text)
    import_data_im('./data/ex_images/AEK/original/')

