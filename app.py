import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import altair as alt
import streamlit as st
import pandas as pd

import plotly.express as px


# Load data
data = pd.read_csv('sgdata.csv')
df = pd.DataFrame(data)

# Config page
st.set_page_config(page_title='Socioeconomic Factors and Income Analysis')

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


st.markdown("""
<div style="font-size: 16px; line-height: 1.6;">
📌 Pada bagian ini merupakan ringkasan temuan utama dari hasil analisis yang dilakukan.  
Isi paragraf ini memberikan gambaran singkat tentang pola-pola yang ditemukan dalam data,  
dan dapat dijadikan referensi awal sebelum masuk ke dashboard analitik yang lebih lengkap.
</div>
""", unsafe_allow_html=True)

# Statistik income
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

# Spacer biar bagian bawah agak turun
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
                **Pendapatan berdasarkan tingkat pendidikan tidak menunjukkan perbedaan yang signifikan.**  
                Rata-rata (*mean*) dan nilai tengah (*median*) di tiap jenjang pendidikan terlihat cukup **berdekatan**,  
                yang mengindikasikan bahwa:

    - 🔍 **Sebaran pendapatan tidak terlalu lebar** dalam tiap kategori pendidikan.
    - 🚫 **Tidak ada nilai ekstrim** yang terlalu memengaruhi rata-rata.
    """, unsafe_allow_html=True)





# Hitung jumlah responden per tingkat pendidikan
education_count = df['Education'].value_counts().reset_index()
education_count.columns = ['Education', 'Count']

# Pie chart
fig_pie = px.pie(
    education_count,
    names='Education',
    values='Count',
    title='Distribution of Respondents by Education Level',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hole=0.5
)

# Atur posisi legend
fig_pie.update_layout(
    legend=dict(
        orientation="h",         
        yanchor="bottom",        
        y=-0.2,                  
        xanchor="center",        
        x=0.5                    
    )
)


mean_by_age = df.groupby('Age')['Income'].mean().reset_index()

top_points = mean_by_age.nlargest(3, 'Income')

line = alt.Chart(mean_by_age).mark_line(point=True).encode(
    x=alt.X('Age', title='Usia'),
    y=alt.Y('Income', title='Pendapatan', scale=alt.Scale(zero=False)),
    tooltip=['Age', 'Income']
)

highlight = alt.Chart(top_points).mark_point(
    size=100,
    filled=True,
    color='crimson'
).encode(
    x='Age',
    y='Income',
    tooltip=['Age', 'Income']
)

labels = alt.Chart(top_points).mark_text(
    align='left',
    dx=5,
    dy=-10,
    fontSize=12,
    fontWeight='bold',
    color='green'
).encode(
    x='Age',
    y='Income',
    text=alt.Text('Income', format=',.0f')
)

chart = (line + highlight + labels).properties(
    title='Rata-rata Pendapatan Berdasarkan Usia',
    width=700,
    height=400
).configure_view(
    stroke=None  
).configure_axis(
    grid=False,  
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=20,
    anchor='start',
    fontWeight='bold'

)

kolom1, kolom2 = st.columns([1.7, 1])  

with kolom1:
    st.markdown("""
        <div style="margin-top: 2rem; font-size: 16px; line-height: 1.6;">
        Jadi, secara umum, <b>disparitas pendapatan antar jenjang pendidikan relatif rendah</b> dalam dataset ini.  
        Tapi perlu diperhatikan bahwa dataset <b>tidak memiliki keseimbangan jumlah responden</b> antar tingkat pendidikan.  
        Hal ini dapat dilihat pada gambar pie chart di samping.
        </div>
    """,unsafe_allow_html=True)

with kolom2:
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()


baru1, baru2 = st.columns([1.5,1])

with baru1:
    st.altair_chart(chart, use_container_width=True)

with baru2:
    st.markdown("""Berdasarkan grafik dapat dilihat bahwa grafik income meningkat seiring denga bertambahnya umur. walaupun ada 
                kondisi dimana eberapa peningkatan umur malah menueurnnya income""")
