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

def GetContents(pathStr, dirFlag=False):

    if pathStr[-1]!="/":
        pathStr+="/"

    # st.write("check",pathStr)
    ### check dir exists
    if not os.path.isdir(pathStr):
        st.write("No directory found")
        st.stop()

    # st.write("all",[pathStr+"/"+f for f in os.listdir(pathStr)])

    ### just files
    if not dirFlag:
        ### keep (only) files
        fileList=[pathStr+f for f in os.listdir(pathStr) if os.path.isfile(pathStr+f)]
        return fileList
    else:
        dirList=[pathStr+f for f in os.listdir(pathStr) if os.path.isdir(pathStr+f)]
        sel_dir=st.selectbox(f"Select from {pathStr}:",dirList, key="sel_"+pathStr)
        try:
            return GetContents(sel_dir, st.checkbox("Get directories?", key="sub_"+pathStr))
        except TypeError:
            st.write("None Found")
            st.stop()

##################
### main part
##################

st.write("## Which directory?")

if "list_dir" not in st.session_state.keys():
    st.session_state['list_dir']=os.getcwd()+"/stuff"
if st.checkbox("Change directory?"):
    st.session_state['list_dir']=st.text_input("Set directory:")


st.write("Using directory path:",st.session_state['list_dir'])
sel_dir=st.checkbox("Get sub-directories")



st.write("---")

st.write("## Contents")

if 1==1: #"contents" not in st.session_state.keys() or st.button("Check again?"):
    # if not os.path.isdir(st.session_state['list_dir']):
    #     st.write("No directory found")
    #     st.stop()
    # ### keep (only) files
    # st.session_state['contents']=[f for f in os.listdir(st.session_state['list_dir']) if os.path.isfile(st.session_state['list_dir']+f)]
    st.session_state['contents']=GetContents(st.session_state['list_dir'], sel_dir)

    st.session_state['file_dict']={}
    for cont in st.session_state['contents']:
        ### skip back-ups
        if "/._" in cont:
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

if len(st.session_state['file_dict'].keys())<1:
    st.write("### None found. Try someting else - get sub-directories?")
    st.stop()

sel_key=st.selectbox("Select file type:",st.session_state['file_dict'].keys())

if sel_key not in st.session_state['file_dict'].keys():
    st.write(f"**Sorry can't find {sel_key}. Try something else.**")

for f in st.session_state['file_dict'][sel_key]:
    ### file name (no path)
    st.write(f.split('/')[-1])
    ## display
    DisplayFile(f,sel_key)
