import streamlit as st
import streamlit.components.v1 as components

st.title("Linear Optimization Calculator (LinOptCalc)")
st.markdown("A versatile implementation of the simplex method for linear optimization that thoroughly documents every step in the optimization process.")

iframe_code="""<iframe src="https://trinket.io/embed/python3/dbf60d5f9ede?outputOnly=true&runOption=run&start=result" width="100%" height="600" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>"""

components.html(iframe_code, height=600)

st.text("")
st.markdown("""*Crafted by yarov3so*   
<a href="https://www.buymeacoffee.com/yarov3so" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 9em; height: auto; padding-top: 0.7em; padding-bottom: 1em" ></a>  
See my other [Math Help Tools](https://mathh3lptools.streamlit.app)""",unsafe_allow_html=True)
