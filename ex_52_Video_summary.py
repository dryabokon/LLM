import tools_DF
import base64
import cv2
import pandas as pd
import yaml
from LLM2 import llm_config
from openai import OpenAI
import imageio
# ----------------------------------------------------------------------------------------------------------------------
import tools_IO
import tools_animation
# ----------------------------------------------------------------------------------------------------------------------
config = llm_config.get_config_openAI()
# ----------------------------------------------------------------------------------------------------------------------
MODEL="gpt-4o"
with open(config.filename_config_chat_model) as config_file:
    config = yaml.safe_load(config_file)
    if 'openai' in config:
        openai_api_key = config['openai']['key']

chatinstance = OpenAI(api_key=openai_api_key)
# ----------------------------------------------------------------------------------------------------------------------
def ex_animation(folder_in):
    filename_out = './data/output/summary.csv'
    pd.DataFrame({"filename": [], "text": []}).to_csv(filename_out, index=False)

    for filename in tools_IO.get_filenames(folder_in, '*.jpg'):
        videoFrames = [base64.b64encode(cv2.imencode(".jpg", image)[1]).decode("utf-8") for image in imageio.get_reader(folder_in+filename)]
        content = ["Images:", *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}},videoFrames)]
        messages = [{"role": "system", "content": "Explain what is happening on the gif animation."},{"role": "user", "content": content}]
        response = chatinstance.chat.completions.create(model=MODEL,temperature=0,messages=messages)
        print(response.choices[0].message.content)
        df = pd.DataFrame({"filename": filename, "text": response.choices[0].message.content}, index=[0])
        df.to_csv(filename_out, mode='a', header=False, index=False)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_video():
    folder_in = './data/ex_images/02/'
    filenames = tools_IO.get_filenames(folder_in, '*.jpg')

    videoFrames = [base64.b64encode(cv2.imencode(".jpg", cv2.imread(folder_in + filename))[1]).decode("utf-8") for filename in filenames]
    content = ["Images:", *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}},videoFrames)]
    messages = [{"role": "system", "content": "Generate a summary from sequence of data points in time."},{"role": "user", "content": content}]

    response = chatinstance.chat.completions.create(model=MODEL,temperature=0,messages=messages)
    print(response.choices[0].message.content)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_series():

    data_points = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    data_string = ", ".join(map(str, data_points))
    prompt = f"Here is a sequence of data points: {data_string}. Please analyze this sequence and describe any patterns or insights."
    messages = [{"role": "user", "content": prompt}]
    response = chatinstance.chat.completions.create(model=MODEL,temperature=0,messages=messages)
    print(response.choices[0].message.content)
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_tabular():
    df = pd.read_csv('./data/ex_datasets/dataset_delivery2.csv').iloc[:10]
    df_str = tools_DF.prettify(df,showindex=False)

    prompt = f"Here is a sequence of data points: {df_str}. Please analyze this sequence and describe any patterns or insights."
    messages = [{"role": "user", "content": prompt}]
    response = chatinstance.chat.completions.create(model=MODEL, temperature=0, messages=messages)
    print(response.choices[0].message.content)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    ex_animation('./data/ex_images/02/')
    #ex_video()
    #ex_series()
    #ex_tabular()
