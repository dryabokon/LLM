import pandas as pd
import cv2
import streamlit as st
import speech_recognition as sr
import sys
# ----------------------------------------------------------------------------------------------------------------------
sys.path.append('../tools/')
sys.path.append('../tools/LLM2/')
import tools_DF
import tools_VertexAI_Search
import tools_image
# ----------------------------------------------------------------------------------------------------------------------
#df = pd.read_csv('./data/ex_datasets/df_LPs.csv')[['track_id','model_color','mmr_type','conf_mmr']]
Vector_Searcher = tools_VertexAI_Search.VertexAI_Search('./secrets/GL/private_config_GCP.yaml','./secrets/GL/ml-ops-poc-695-331cbd915e34.json')
Vector_Searcher.table_name = 'AEK'
# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
def recognize_speech_from_mic(placeholder_status):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        placeholder_status.text("Listening...")
        audio = recognizer.listen(source)

    try:
        placeholder_status.text("Recognizing speech...")
        command = recognizer.recognize_google(audio)
        return command
    except sr.UnknownValueError:
        placeholder_status.text("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        placeholder_status.text(f"Could not request results from Google Speech Recognition service; {e}")
        return None
# ----------------------------------------------------------------------------------------------------------------------
def run_query(query,select,limit=4):

    df = Vector_Searcher.search_vector(query, select=select, as_df=True, limit=2*limit)
    if df.shape[0] == 0:return 'No results found',[]
    if df.shape[0] == 0: return 'No relevant results found',[]

    df = df.sort_values(by='score', ascending=True)[:limit]
    res_txt = tools_DF.prettify(df, showindex=False)
    images = [cv2.imread('./data/ex_images/AEK/profile_%04d.png'%i) for i in df['track_id'].values]
    images = [tools_image.smart_resize(im,target_image_height=320) if im is not None else None for im in images]

    return res_txt, images
# ----------------------------------------------------------------------------------------------------------------------
def ex_streamlit():

    st.title("Gen AI | LLM chat bot")
    placeholder_option = st.radio("", ("Text Input","Voice Command"),horizontal=True)
    placeholder_button = st.empty()
    placeholder_status = st.empty()
    placeholder_query = st.empty()
    placeholder_res_txt = st.empty()
    res_row0,res_row1,res_row2,res_row3 = st.empty(),st.empty(),st.empty(),st.empty()

    command = None

    if placeholder_option == "Voice Command":
        if placeholder_button.button("Start Listening"):
            command = recognize_speech_from_mic(placeholder_status)
            placeholder_query.write(f"Recognized Command: {command}")
    else:
        placeholder_button.empty()
        placeholder_status.empty()
        command = placeholder_query.text_input("")

    if command:
        res_text, images = run_query(command,select=['track_id','text','score'])
        placeholder_res_txt.text(res_text)

        for i,im in enumerate(images):
            if im is None: continue
            if i == 0: res_row0.image(im[:, :, [2, 1, 0]], caption='Result %d' % i, use_column_width=True)
            if i == 1: res_row1.image(im[:, :, [2, 1, 0]], caption='Result %d' % i, use_column_width=True)
            if i == 2: res_row2.image(im[:, :, [2, 1, 0]], caption='Result %d' % i, use_column_width=True)
            if i == 3: res_row3.image(im[:, :, [2, 1, 0]], caption='Result %d' % i, use_column_width=True)

    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #ex_streamlit()

    html_data = '''<!DOCTYPE html>
<html lang="en">
<body>
    <div class="camera-feed">
        <h1>Hello Dima!</h1>
    </div>
</body>
</html>'''

    st.markdown(html_data, unsafe_allow_html=True)
