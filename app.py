import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import altair as alt
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px



# Load data
data = pd.read_csv('sgdata.csv')
df = pd.DataFrame(data)

# Config page
st.set_page_config(page_title='Socioeconomic Factors and Income Analysis')



kolom_profil, kolom_about = st.columns([1, 2])

# Kolom kiri: Foto Profil
with kolom_profil:
    img_profil = Image.open('Business_Casual_Alt_3_3_1738636868680.png')
    st.image(img_profil, caption='👨‍💼 Hi, guys!', use_column_width=True)

# Kolom kanan: Tentang Saya
with kolom_about:
    st.markdown("""
    ### 🙋‍♂️ Hello There!
    My name is **[Your Name Here]**, and I'm passionate about **data, design, and digital innovation**.

    - 📊 Data Enthusiast  
    - 🧠 Lifelong Learner  
    - 💬 Always curious and open to collaboration  

    > *"Code is poetry, and data tells the story."*

    Let's connect and create something amazing together! 🌟
    """)
    
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2025 My Awesome Streamlit App</p>", unsafe_allow_html=True)
    

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

col1, col2 = st.columns([1.5, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
                Pendidikan yang lebih tinggi berhubungan dengan pendapatan yang lebih tinggi. Orang yang memiliki pendidikan universitas (S1) dan graduate school cenderung memiliki 
                pendapatan yang jauh lebih tinggi, sekitar 35.000, dibandingkan dengan mereka yang hanya memiliki pendidikan SMA.
                <br></br>
                Menarik juga bahwa sebaran pendapatan dalam tiap kategori pendidikan tidak terlalu lebar. Hal itu dibuktikan dengan apa?
                ya, mean dan mediannya tidak jauh berbeda di tiap kategori. hal ini menunjukkan bahwa
                tidak ada nilai ekstrim tertentu yang berpengaruh signifikan
                terhadap rata rata yang kita hitung.
                <br></br>
                Jadi, dapat dikatakan bahwa, <b>semakin tinggi tingkat pendidikan maka semakin tinggi pula rata-rata pendapatannya. Dan, pendapatan di tiap jenjang juga tidaklah jauh berbeda</b>.-

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
    color='white'
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
    color='white',
    fontWeight='bold'

)

chart2 = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('Age:Q', title='Age', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),
    y=alt.Y('Income:Q', title='Income', axis=alt.Axis(grid=False), scale=alt.Scale(zero=False)),
    color=alt.Color(
        'Occupation:N',
        legend=alt.Legend(
            orient='bottom',
            direction='vertical',
            labelLimit=500,  # Mengatur panjang label agar tidak terpotong
            title=None       # Menghilangkan judul legenda jika tidak perlu
        )
    ),
    tooltip=['Age', 'Income', 'Occupation']
).interactive().properties(
    title='Distribusi Income Berdasarkan Umur dan Pekerjaan',
    width=500,   # Lebar chart disesuaikan agar tidak terpotong
    height=400    # Tinggi chart yang sesuai
).configure_view(
    continuousHeight=400,
    continuousWidth=500
)


kolom1, kolom2 = st.columns([1.7, 1])  

with kolom1:
    st.markdown("""
        <div style="margin-top: 2rem; font-size: 16px; line-height: 1.6;">
        Selain itu, perhatikan bahwa. Distribusi tingkat pendidikan dalam data ini belum merata—hanya sekitar 14% yang 
        memiliki pendidikan universitas, dan bahkan hanya 1,8% yang menempuh graduate school. Meski begitu, kelompok kecil ini justru 
        menunjukkan rata-rata pendapatan yang lebih tinggi dibandingkan jenjang lainnya. Apabila distribusi tingkat pendidikan lebih seimbang, maka gambaran rata-rata pendapatan secara 
        keseluruhan pun bisa berubah secara signifikan. Artinya, semakin banyak orang yang mengenyam pendidikan tinggi, 
        bisa jadi rata-rata pendapatan secara umum juga akan meningkat.
        </div>
    """,unsafe_allow_html=True)
    st.divider()
    st.altair_chart(chart2, use_container_width=True)

with kolom2:
    st.plotly_chart(fig_pie, use_container_width=True)
    st.divider()
    st.altair_chart(chart, use_container_width=True)


st.divider()



