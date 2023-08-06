# Import packages
from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dataclasses import dataclass
from PIL import Image
import io
import os
import base64

@dataclass
class ManagementResult:
    pass

def convert_df(csv_file):
    '''
    Reading a csv file
    Args:
        template_df - filename of template
    Returns:
        template_df in csv format
    '''
    template_df = pd.read_csv(csv_file)
    return template_df.to_csv().encode('utf-8')


def read_image_file(image_file):
    '''
    Reading a image file
    Args:
        image_file - filename of Image template 
    Returns:
        image_file in array format
    '''
    image = Image.open(
        image_file)  # template screenshot provided as an example
    return image


def display_download(image_file, csv_file):
    '''
    Displaying a template image and giving download option to download csv file
    Args:
        image_file - filename of Image template 
        csv_file - filename of template
    Returns:
        Returns template Image
        giving download option to download csv file
    '''
    st.markdown("<h1 style='text-align: center; color: blue;'>Dr.Management</h1>",
                unsafe_allow_html=True)
    # Add a template screenshot as an example
    st.subheader('Step 1: Download the project plan template')
    image = read_image_file(image_file)
    st.image(
        image,  caption='Make sure you use the same column names as in the template')
    # Allow users to download the template
    csv = convert_df(csv_file)
    st.download_button(
        label="Download Template",
        data=csv,
        file_name='project_template.csv',
        mime='text/csv',
    )


def project_mngt(image_file, csv_file):
    '''
    Args:
    image_file -  filename of Image template
    csv_file -  filename of template
    Returns:
    '''
    display_download(image_file, csv_file)

    # Add a file uploader to allow users to upload their project plan file
    st.subheader('Step 2: Upload your project plan file')

    uploaded_file = st.file_uploader(
        "Fill out the project plan template and upload your file here. \
         After you upload the file, you can edit #your project plan within the app.", type=['csv'])
    if uploaded_file is not None:
        Tasks = pd.read_csv(uploaded_file)
        Tasks['Start'] = Tasks['Start'].astype('datetime64')
        Tasks['Finish'] = Tasks['Finish'].astype('datetime64')

        grid_response = AgGrid(
            Tasks,
            editable=True,
            height=300,
            width='100%',
        )

        updated = grid_response['data']
        template_df = pd.DataFrame(updated)

    else:
        st.warning('You need to upload a csv file.')

    # Main interface - section 3
    st.subheader('Step 3: Generate the Gantt chart')

    Options = st.selectbox("View Gantt Chart by:", [
                           'Team', 'Completion Pct'], index=0)
    if st.button('Generate Gantt Chart'):
        fig = px.timeline(
            template_df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color=Options,
            hover_name="Task Description"
        )

        # if not specified as 'reversed', the tasks will be listed from bottom up
        fig.update_yaxes(autorange="reversed")

        fig.update_layout(
            title='Project Plan Gantt Chart',
            hoverlabel_bgcolor='#DAEEED',
            bargap=0.2,
            height=600,
            xaxis_title="",
            yaxis_title="",
                        title_x=0.5,  # Make title centered
            xaxis=dict(
                tickfont_size=15,
                tickangle=270,
                rangeslider_visible=True,
                side="top",  # Place the tick labels on the top of the chart
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
                tickformat="%x\n",  #
            )
        )

        fig.update_xaxes(tickangle=0, tickfont=dict(
            family='Rockwell', color='blue', size=15))

        # Display the plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Allow users to export the Plotly chart to HTML
        st.subheader(
            'Bonus: Export the interactive Gantt chart to HTML and share with others!')
        buffer = io.StringIO()
        fig.write_html(buffer, include_plotlyjs='cdn')
        html_bytes = buffer.getvalue().encode()
        st.download_button(
            label='Export to HTML',
            data=html_bytes,
            file_name='Gantt.html',
            mime='text/html'
        )