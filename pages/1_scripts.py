import streamlit as st

import os
import sys
import json
import subprocess
import altair as alt
import pandas as pd

### introduction
st.title('Lister App')
st.write('### List things')
st.write("---")


##################
### useful funcitons
##################

def DisplayFile(file,ext):

    if ext in ['png','svg','jpg','jpeg','gif']:
        st.image(file)
    elif ext in ['ogg','wav','mp3','mp4','m4a']:
        st.audio(file)
    elif ext!="no_ext":
        st.write("__Read contents:__")
        with open(file, "r") as f:
            data = f.read()
            st.write(data)
    else:
        st.write("No extension")


##################
### main part
##################

st.write("## Which directory?")

if "list_dir" not in st.session_state.keys():
    st.session_state['list_dir']=os.getcwd()+"/stuff"
if st.checkbox("Change directory?"):
    st.session_state['list_dir']=st.text_input("Set directory:")

if st.session_state['list_dir'][-1]!="/":
    st.session_state['list_dir']+="/"

st.write("Using directory path:",st.session_state['list_dir'])


st.write("---")

st.write("## Contents")

if "contents" not in st.session_state.keys() or st.button("Check again?"):
    if not os.path.isdir(st.session_state['list_dir']):
        st.write("No directory found")
        st.stop()
    st.session_state['contents']=os.listdir(st.session_state['list_dir'])

    st.session_state['file_dict']={}
    for cont in st.session_state['contents']:
        if cont[0:2]=="._":
            continue
        if "." not in cont:
            try:
                st.session_state['file_dict']['no_ext'].append(cont)
            except KeyError:
                st.session_state['file_dict']['no_ext']=[cont]
        else:
            cont_ext=cont.split('.')[-1]
            try:
                st.session_state['file_dict'][cont_ext].append(cont)
            except KeyError:
                st.session_state['file_dict'][cont_ext]=[cont]

st.write("files found:",len(st.session_state['contents']))
st.write("-",len(st.session_state['file_dict'].keys()),"file types")

if st.checkbox("See file list?"):
    st.write(st.session_state['contents'])

st.write("---")

sel_key=st.selectbox("Select file type:",st.session_state['file_dict'].keys())

for f in st.session_state['file_dict'][sel_key]:
    st.write(f)
    DisplayFile(st.session_state['list_dir']+f,sel_key)
