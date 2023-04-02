import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My parents new healthy diner");

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard-Boiled Free-Range Egg')
   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice )      
   # write your own comment -what does the next line do? 
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')   
   if not fruit_choice:
      streamlit.error("Erreur merci de mettre un fruit")
   else:
      back_from_function=get_fruityvice_data(fruit_choice)
      # write your own comment - what does this do?
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()

#streamlit.write('The user entered ', fruit_choice)
#streamlit.text(fruityvice_response.json())


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)
#my_cur.execute("select * from fruit_load_list")
#my_data_raw= my_cur.fetchall()

streamlit.header("fruit liste contains:")
def get_list_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()

if streamlit.button('get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_raw = get_list_load_list()
   my_cnx.close()
   streamlit.dataframe( my_data_raw );                

#streamlit.text("liste druit:")
#streamlit.text(my_data_raw)
#streamlit.stop()

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values('" +new_fruit+"');")
      return "Thanks for adding " + new_fruit
   
add_my_fruit = streamlit.text_input('Quel fruit veux tu ajouter')

if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_my_fruit)
   streamlit.text( back_from_function );
   
#streamlit.write('The user entered ', fruit_choice1)
#streamlit.write('merci d\'avoir ajouter le fruit  ', fruit_choice1)
#my_cur.execute("insert into fruit_load_list values('from streamlit');")
#my_cur.execute("insert into fruit_load_list values(\'"+ fruit_choice1 +" \');")
