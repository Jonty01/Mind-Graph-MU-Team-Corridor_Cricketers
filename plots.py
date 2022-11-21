import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

st.title('Student Profile Analysis')
# energy_source = pd.DataFrame({
#     "EnergyType": ["Electricity","Gasoline","Natural Gas","Electricity","Gasoline","Natural Gas","Electricity","Gasoline","Natural Gas"],
#     "Price ($)":  [150,73,15,130,80,20,170,83,20],
#     "Date": ["2022-1-23", "2022-1-30","2022-1-5","2022-2-21", "2022-2-1","2022-2-1","2022-3-1","2022-3-1","2022-3-1"]
#     })

# option = st.selectbox(
#      'Select type',
#      ('Clubs participants data', 'Fest participants data','Clubs organisers data','Fest organisers data','No of participants in fests 1 and fest 2 from club 1','No of participants in fests 1 and fest 2 from club 2','No of participants in fests 1 and fest 2 from club 3','No of students participating in various events in fest 1','No of students participating in various events in fest 2','No of students participating in various events in various clubs'))
# # keep the option and select boxes on the left side of the screen

# make an option box at the left side of the screen
option = st.sidebar.selectbox(
        'Select type',
        ('Clubs participants and organisers data', 'Fest participants and organisers data','No of participants in fests 1 and fest 2 from club 1','No of participants in fests 1 and fest 2 from club 2','No of participants in fests 1 and fest 2 from club 3','No of students participating in various events in fest 1','No of students participating in various events in fest 2','No of students participating in various events in various clubs'))



if option == 'Clubs participants and organisers data':
    "Participants data in clubs"
    source = pd.DataFrame({
        'Participants': [322,325,325],
        'Total': ['Club1','Club2','Club3'],
     })
 
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Total',
        x='Participants',
    )
    st.altair_chart(bar_chart, use_container_width=True)

    "Organisers Data in clubs"
    source = pd.DataFrame({
        'Organisers': [15,15,15],
        'Total': ['Club1','Club2','Club3'],
     })
 
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Total',
        x='Organisers',
    )
 
    st.altair_chart(bar_chart, use_container_width=True)

elif option == 'Fest participants and organisers data':
    "Participants data in fests"
    source = pd.DataFrame({
        'Participants': [1853,2552],
        'Total': ['Fest_1','Fest_2'],
     })

    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Total',
        x='Participants',
    )
    st.altair_chart(bar_chart, use_container_width=True)

    "Organisers data for clubs"
    source = pd.DataFrame({
        'Organisers': [72,83],
        'Total': ['Fest1','Fest2'],
     })
 
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Total',
        x='Organisers',
    )

    st.altair_chart(bar_chart, use_container_width=True)

    # code = '''  "Energy Costs By Month"
    # source = pd.DataFrame({
    #     'Price ($)': [10, 15, 20],
    #     'Month': ['January', 'February', 'March']
    # })
 
    # bar_chart = alt.Chart(source).mark_bar().encode(
    #     y='Price ($)',
    #     x='Month',
    # )
    # st.altair_chart(bar_chart, use_container_width=True)
    #  '''
    # st.code(code, language='python')
# elif option == 'Clubs organisers data':
#     "Organisers data for clubs"
#     source = pd.DataFrame({
#         'Organisers': [15,15,15],
#         'Total': ['Club1','Club2','Club3'],
#      })
 
#     bar_chart = alt.Chart(source).mark_bar().encode(
#         y='Total',
#         x='Organisers',
#     )
 
#     st.altair_chart(bar_chart, use_container_width=True)


# elif option == 'Fest organisers data':
#     "Organisers data for clubs"
#     source = pd.DataFrame({
#         'Organisers': [72,83],
#         'Total': ['Fest1','Fest2'],
#      })
 
#     bar_chart = alt.Chart(source).mark_bar().encode(
#         y='Total',
#         x='Organisers',
#     )
 
#     st.altair_chart(bar_chart, use_container_width=True)


elif option == 'No of participants in fests 1 and fest 2 from club 1':
    "No of participants in fests 1 and fest 2 from club 1"
    labels = 'Fest_1', 'Fest_2'
    sizes = [40.83, 59.17]
    #explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

elif option == 'No of participants in fests 1 and fest 2 from club 2':
    "No of participants in fests 1 and fest 2 from club 2"
    labels = 'Fest_1', 'Fest_2'
    sizes = [41.654, 58.346]
    #explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

elif option == 'No of participants in fests 1 and fest 2 from club 3':
    "No of participants in fests 1 and fest 2 from club 3"
    labels = 'Fest_1', 'Fest_2'
    sizes = [40.58, 59.42]
    #explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

elif option == 'No of students participating in various events in fest 1':
    "participants in fest 1 events"
    source = pd.DataFrame({
        'No of students': [203,206,207,205,200,139,138,138,142,138,137,136,142],
        'Events': ['Event1','Event2','Event3','Event4','Event5','Event6','Event7','Event8','Event9','Event10','Event11','Event12','Event13'],
     })

    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Events',
        x='No of students',
    )
 
    st.altair_chart(bar_chart, use_container_width=True)
elif option == 'No of students participating in various events in fest 2':
    "participants in fest 2 events"
    source = pd.DataFrame({
        'No of students': [209,203,205,205,205,140,142,137,142,143,140,141,140,138,139],
        'Events': ['Event1','Event2','Event3','Event4','Event5','Event6','Event7','Event8','Event9','Event10','Event11','Event12','Event13','Event14','Event15'],
     })
 
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Events',
        x='No of students',
    )

    st.altair_chart(bar_chart, use_container_width=True)



elif option == 'No of students participating in various events in various clubs':
    "participants in club 1 events"
    # source = pd.DataFrame({
    #     'No of students': [134, 136, 67],
    #     'Events': ['Event1','Event2','Event3'],
    #  })
    source = pd.DataFrame({
        'No of students': [134, 136, 67],
        'Events': ['Event1','Event2','Event3'],
        'Club': ['Club1','Club1','Club1']
    })
    
    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Events',
        x='No of students',
        color='Club'
    )

    st.altair_chart(bar_chart, use_container_width=True)

    "participants in club 2 events"
    source = pd.DataFrame({
        'No of students': [138, 138, 64],
        'Events': ['Event1','Event2','Event3'],
        'Club': ['Club2','Club2','Club2']
    })

    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Events',
        x='No of students',
        color='Club'
    )
 
    
    st.altair_chart(bar_chart, use_container_width=True)

    "participants in club 3 events"
    source = pd.DataFrame({
        'No of students': [138, 136, 66],
        'Events': ['Event1','Event2','Event3'],
        'Club': ['Club3','Club3','Club3']
    })

    bar_chart = alt.Chart(source).mark_bar().encode(
        y='Events',
        x='No of students',
        color='Club'
    )
    
    st.altair_chart(bar_chart, use_container_width=True)
    
 
    # bar_chart = alt.Chart(source).mark_bar().encode(
    #     y='Events',
    #     x='No of students',
    # )
 
    # st.altair_chart(bar_chart, use_container_width=True)
