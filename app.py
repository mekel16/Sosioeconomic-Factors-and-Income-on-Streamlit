import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import altair as alt
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

data = pd.read_csv('D:\Download\sgdata.csv')
df = pd.DataFrame(data)

st.set_page_config(page_title='Socioeconomic Factors and Income Analysis')

kolom_profil, kolom_about = st.columns([1, 2])

with kolom_profil:
    img_profil = Image.open("D:\Download\Business_Casual_Alt_3_3_1738636868680.png")
    st.image(img_profil, use_container_width=True)

with kolom_about:
    st.markdown("""
    ### 🙋‍♂️ Hello There!
    My name is **Michael Pallea'**, and I'm passionate about **data, Machine Learning, DeepLearning and Web Design**.

    - 📊 Data Enthusiast  

    > *"only God we Trust, all other must bring data"*

    Let's connect and create something amazing together! 🌟
    see my portofolio here :
    *https://michpalleaportfolio.carrd.co/*
    """)
    
st.markdown("---")    

st.markdown("""
    <style>
        .block-container {
            max-width: 90vw;    
            width: 100%;
            max-width: 1000px;    
            margin: 0 auto;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)



# Title
st.title('Socioeconomic Factors and Income Analysis')
st.write('the dataset i got from here: *https://www.kaggle.com/datasets/aldol07/socioeconomic-factors-and-income-dataset/data*')


st.markdown("""
<div style="font-size: 16px; line-height: 1.6;">

</div>
""", unsafe_allow_html=True)

mean_by_education = df.groupby('Education')['Income'].mean()
median_by_education = df.groupby('Education')['Income'].median()

income_stats = pd.DataFrame({
    'Education': mean_by_education.index,
    'Mean Income': mean_by_education.values,
    'Median Income': median_by_education.values
})

# Chart: Mean vs Median
fig = go.Figure()
fig.add_trace(go.Bar(
    x=income_stats['Education'],
    y=income_stats['Mean Income'],
    name='Mean Income',
    marker_color='rgba(100,149,237, 0.85)',
    hovertemplate='Mean: %{y}<extra></extra>'
))
fig.add_trace(go.Bar(
    x=income_stats['Education'],
    y=income_stats['Median Income'],
    name='Median Income',
    marker_color='rgba(144,238,144, 0.85)',
    hovertemplate='Median: %{y}<extra></extra>'
))

fig.update_layout(
    barmode='group',
    title='Income Comparison by Education Level',
    xaxis_title='Education Level',
    yaxis_title='Income',
    template='plotly_white',
    legend=dict(x=0.7, y=1.1),
    margin=dict(l=40, r=40, t=60, b=40),
)

st.divider()

st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
                **Higher education is linked to higher income levels**. 
                Individuals with a university education (Bachelor's degree) and those with graduate degrees tend to earn significantly more, 
                with average incomes around **$35.000**, compared to those with only a high school diploma.
                <br></br>
                Note that, the income distribution within each education category is **relatively narrow**. 
                The *mean* and *median* incomes in each category are quite similar, indicating that there are *no extreme values significantly affecting the average* income we calculated.
                <br></br>
                Higher education levels typically lead to higher average incomes, 
                and income variations within each education level are minimal.

    """, unsafe_allow_html=True)


education_count = df['Education'].value_counts().reset_index()
education_count.columns = ['Education', 'Count']

fig_pie = px.pie(
    education_count,
    names='Education',
    values='Count',
    title='Distribution of Respondents by Education Level',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hole=0.5
)

fig_pie.update_layout(
    legend=dict(
        orientation="h",         
        yanchor="bottom",        
        y=-0.2,                  
        xanchor="center",        
        x=0.5                    
    )
)

df_grouped = df.groupby(['Age', 'Sex'])['Income'].mean().reset_index()
chart_detail = alt.Chart(df_grouped).mark_line().encode(
    x=alt.X('Age:Q', title='Age', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),    
    y=alt.Y('Income:Q', title='Income', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),
    color='Sex:N',
    tooltip=['Age', 'Income', 'Sex']

).properties(
    title='Income by Age and Sex',
    width=700,
    height=400   
).interactive()

chart2 = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('Age:Q', title='Age', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),
    y=alt.Y('Income:Q', title='Income', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),
    color=alt.Color(
        'Occupation:N',
        legend=alt.Legend(
            orient='bottom',
            direction='vertical',
            labelLimit=500,  
            title=None     
        )
    ),
    tooltip=['Age', 'Income', 'Occupation']
).properties(
    title='Income by Age and Occupation',
    width=700,
    height=400 
).interactive()

kolom1, kolom2 = st.columns([1.7, 1])  

with kolom1:
    st.markdown("""
        <div style="margin-top: 2rem; font-size: 16px; line-height: 1.6;">
        It's important to note that, the distribution of education levels in this data is uneven. 
        Only about 14% of individuals hold a university degree, and among them, just 1.8% have pursued graduate studies. 
        However, this smallgroup exhibits a higher average income compared to those with lower education levels. If the distribution of education levels were more balanced, 
        the overall average income could change significantly. 
        This suggests that as more people attain higher education, the average income across the population may also rise.
        <br></br>
        <br></br>

        </div>
    """,unsafe_allow_html=True)

with kolom2:
    st.plotly_chart(fig_pie, use_container_width=True)

col_avg_by_age, col_text_by_age = st.columns([2,0.8])

with col_avg_by_age:
    st.altair_chart(chart_detail, use_container_width=True)

with col_text_by_age:
    st.markdown("""Analyzing demographics by age and gender reveals that older age does not equate to higher income for either gender. 
            Let's explore additional demographic factors as follows.""")

st.altair_chart(chart2, use_container_width=True)

st.divider()


