import streamlit as st
import streamlit.components.v1 as components

iframe_code="""<iframe src="https://trinket.io/embed/python3/a57e81eabcb8?outputOnly=true&runOption=console&start=result" width="100%" height="356" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>"""

components.html(iframe_code, height=600)
