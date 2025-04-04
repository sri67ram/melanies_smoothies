# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits from lists:")

name_on_order = st.text_input("Name of smoothie:")
st.write("The name of your smoothie will be :", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe
   , max_selections =5
)

if ingredients_list:

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_list += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients) 
                        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")  
