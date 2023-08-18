import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('salarypredict_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor=data["model"]
le_country=data["le_country"]
le_education=data["le_education"]


def predict_page():
    st.title("Predict Software Engineer Salary")
    st.write("### Please input information to predict the salary:")
    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "India",
        "France",
        "Netherlands",
        "Australia",
        "Brazil",
        "Spain",
        "Sweden",
        "Italy",
        "Poland",
        "Switzerland",
        "Denmark",
        "Norway",
        "Israel",
        "Portugal",
        "Austria",
        "Finland",
        "Belgium",
        "Russian Federation",
        "New Zealand",
        "Ukraine",
        "Turkey",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Professional degree",
    )
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience",0,50,3)
    submit = st.button("Predict Salary")
    if submit:
        # Country, Age,,EdLevel,YearsCodePro
        x = np.array([[25,country, education, experience]])
        x[:, 1] = le_country.transform(x[:, 1])
        x[:, 2] = le_education.transform(x[:, 2])
        x = x.astype(float)

        salary = regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:2f}")