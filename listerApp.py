import streamlit as st

import os


### introduction
st.title('🙂 Lister webApp')
st.write("---")

### contents
st.write("## Contents")
pyFiles=[f for f in os.listdir(os.getcwd()+"/pages") if ".py" in f] 
pyFiles=sorted(pyFiles)
for e,pf in enumerate(pyFiles,1):
    st.write(f" {e}. {pf}")

st.write("---")
