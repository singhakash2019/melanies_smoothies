# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests




# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name of your smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list= st.multiselect(
    'choose upto 5 ingredeitns:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string+=fruits_chosen+' '
        st.subheader(fruits_chosen+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruits_chosen)
        fv_st=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    

if ingredients_list:
    ingredients_string='' 
    for i in ingredients_list:
        ingredients_string=ingredients_string+i+' ';
    
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
    values ('""" + ingredients_string +"""','"""+name_on_order+ """')"""
    time_to_insert= st.button('Submit order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

