import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

st.title('AirBnb Analysis')

data = pd.read_csv(r'F:\GUVI_DATA_SCIENCE\Project\AirBnb_Analysis\airbnb_data.csv')

aggregated = data.groupby(['country','city']).count()

country_in = st.selectbox('Select a Country',options=data['country'].unique())

if country_in == 'Australia':
    city_in = st.selectbox('Select a City',options=['Sydney'])

elif country_in == 'Brazil':
    city_in = st.selectbox('Select a City',options=['Rio De Janeiro','Other (International)'])

elif country_in == 'Canada':
    city_in = st.selectbox('Select a City',options=['Montreal'])

elif country_in == 'China':
    city_in = st.selectbox('Select a City',options=['Hong Kong'])

elif country_in == 'Hong Kong':
    city_in = st.selectbox('Select a City',options=['Hong Kong'])

elif country_in == 'Portugal':
    city_in = st.selectbox('Select a City',options=['Porto','Other (International)'])

elif country_in == 'Spain':
    city_in = st.selectbox('Select a City',options=['Barcelona'])

elif country_in == 'Turkey':
    city_in = st.selectbox('Select a City',options=['Istanbul','Other (International)'])

elif country_in == 'United States':
    city_in = st.selectbox('Select a City',options=['Kauai','Maui','New York','Oahu','The Big Island','Other (Domestic)'])


min_price = st.text_input('Select a Minimum Price')
max_price = st.text_input('Select a Maximum Price')

query_df = data.query(f'country == "{country_in}" and city == "{city_in}" and price>={min_price} and price<={max_price}')
reset_index = query_df.reset_index(drop = True)

# Creating map using folium
base_latitude = reset_index.loc[0,'latitude']
base_longitude = reset_index.loc[0,'longitude']

base_map = folium.Map(location=[base_latitude,base_longitude], zoom_start=12)

for index, row in reset_index.iterrows():
    lat,lon = row['latitude'],row['longitude']
    id = row['id']
    name = row['name']
    price = row['price']
    review = row['review_score']
    popup_text = f"ID: {id} | Name: {name} | Price: ${price} | Rating: {review}/10"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(base_map)

# call to render Folium map in Streamlit
st_data = st_folium(base_map, width=1200,height = 600)

st.subheader('Top 5 Hotels Recommendation')

df = reset_index.sort_values(by=['price','review_score','no_of_reviews'],ascending = False)

new_df = df[['id','url','name','city','country','amenities','price','review_score','no_of_reviews']]

blankIndex=[''] * len(new_df)
new_df.index=blankIndex
st.dataframe(new_df.head())

st.subheader('Enter the ID to fetch detailed information')

id_input = st.text_input('Enter a ID')

new_query = reset_index.query(f'country == "{country_in}" and city == "{city_in}" and price>={min_price} and price<={max_price} and id == {int(id_input)}')
