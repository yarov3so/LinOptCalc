import streamlit as st
import streamlit.components.v1 as components

iframe_code="""<iframe src="https://trinket.io/python3/a57e81eabcb8?outputOnly=true&runOption=run&showInstructions=true" width="100%" height="150em" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>"""

components.html(iframe_code, height=600)
