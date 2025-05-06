import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



# Configure Streamlit page
st.set_page_config(
    page_title="Workout Visualizer",
)
class Person:
    def __init__(self,name):
        self.name=name
        
    def getAxes(self,workout,set_and_nums):
        #workout:str
        #set_and_num:[[number_of_set,s1,s2...]]
        def getIntensity(set_and_num,set_intensity=0.3,set_count_intensity=0.1):
            intensity = 0
            num_sets=set_and_num[0]
            for i in range(num_sets):
                intensity+=(((num_sets-i)*set_intensity+num_sets)/num_sets)*set_and_num[i+1]
            intensity+=set_count_intensity*num_sets
            return intensity
                
        y=np.array([getIntensity(s) for s in set_and_nums])
        x=np.arange(1,len(set_and_nums)+1,1)
        return x,y

    def getCharts(self,data,days):
        #data :{"workout name":sets_and_nums}
        #days :[str,str...
        # Create a figure and a grid of subplots (2 rows, 3 columns)
        fig, axes = plt.subplots(5, 1, figsize=(12, 8))

        #set title
        fig.suptitle(self.name)
        
        # Adjust the layout to prevent overlap
        fig.tight_layout(pad=3.0)

        #positons
        left, width = .0,1
        bottom, height = .25, .75
        right = left + width
        top = bottom + height

        #get axes
        x=[]
        y=[]
        for i,_ in enumerate(data.items()):
            k,v=_
            tmp_x,tmp_y=self.getAxes(k,v)
            x.append(tmp_x)
            y.append(tmp_y)

        workouts=list(data.keys())
        
        # Plot the scatter plots in the subplots
        for i in range(len(x)):
            row = i   # Integer division to determine the row index
            axes[row].scatter(x[i], y[i])
            axes[row].text(left,top,workouts[i],
                horizontalalignment='left',
                verticalalignment='top',
                transform=axes[row].transAxes)
        # Show the plot
        st.pyplot(fig)
        
test_person=Person('Heeyoung')
test_person2=Person('Han')
#test getAxes()
'''x,y=test_person.getAxes('bridge',[[1,10],[2,15,10]])
st.write(x,y)'''

#test getCharts()
test_person.getCharts({'bridge':[[1,10],[2,15,10],[3,10,10,10]],'pullup':[[1,10],[2,15,10],[0]]},['4/1','4/2','4/3'])
test_person2.getCharts({'bridge':[[1,10],[2,15,10],[3,10,10,10]],'pullup':[[1,10],[2,15,10],[0]]},['4/1','4/2','4/3'])



_MY_TOKEN = "ntn_E57599441475dxDyNy7EPrceaxLlKI3mng7Rsl2QktdgID"
_PAGE_URL ="https://www.notion.so/Workout-Tracker-1d515751c5d38018a3e5fd9b844f9be0?pvs=4"
from streamlit_notion import NotionConnection
import os
from notion_client import Client

os.environ['NOTION_API_KEY']=_MY_TOKEN
notion = Client(auth=os.environ['NOTION_API_KEY'])
# Create connection
conn = st.connection("notion", type=NotionConnection)

databases = conn.list_databases()
workout_archive=databases["results"][0]
pages = conn.query(workout_archive["id"])

for p in pages:
    st.write(p)

