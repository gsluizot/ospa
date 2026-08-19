import streamlit as st

github_url = "https://github.com/gsluizot/ospa"
linkedin_url = "https://www.linkedin.com/in/luiz-otavio-gomes-soares-oliveira-10b943198/"

st.title("Prepare the structure of your Human Resources Datalake. Everything in your PC.")

about_tab, how_tab, get_started_tab = st.tabs(["About the project", "How it works", "Get Started"])

with about_tab:
    st.subheader("About the project")

    st.markdown(f"""
    This project utilizes open source technologies to structure a human resources datalake. 
    We disponibilize a step-by-step model with all the necessary data, as well as all the 
    pipelines that you'll need to apply to better structure it.

    You can personalize the structure anyway you want (seriously, you can fork everything 
    and be free). [Repository on GitHub]({github_url}).
    """)

    st.markdown(f"""
    If you find this project useful, please consider following me on 
    [LinkedIn]({linkedin_url}). Hope you enjoy it! s2
    """)

with how_tab:
    pass