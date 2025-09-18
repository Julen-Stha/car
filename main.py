#importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def load_data(data_path:str):
    df = pd.read_csv(data_path)
    return df

df = load_data("Data/car.csv")
st.set_page_config("Fpl Data Analysis")

st.title("Data Dashboard")

# st.write("Python")
# st.write(["Python","JS","Java"])
# st.markdown("## Sample Data")
# st.write(df.head())
# st.divider()
# st.dataframe(df.head())

def filter_transmission(df, column_value:str):
    custom_filter = df["Transmission"] == column_value
    filtered_df  = df[custom_filter]
    return filtered_df

def filter_Price(df, column_value:str):
    custom_filter = df["Price"] <= column_value
    filtered_df  = df[custom_filter]
    return filtered_df


def filter_rangePrice(df, start_price, end_price):
    custom_filter = df[
        (df['Price'] >= start_price) & (df['Price'] <= end_price)

    ] 
    return custom_filter


with st.sidebar:
    #select box
    option = st.selectbox("What would you like to select:",
        (df.Transmission.unique()),index=None
    )

    st.divider()
    
    #for slider
    price = st.slider("Price", min_value=df.Price.min(), max_value=df.Price.max(),step = 10,label_visibility="visible", width="stretch")

    st.divider()

    #range slider
    start_price, end_price = st.slider("Select a range of values", min_value=df.Price.min(), max_value=df.Price.max(),value = (df.Price.min(),df.Price.max()))

    st.divider()
    
    #for text input
    number_price = st.number_input("Enter Price:",step = 1000, min_value = df.Price.min(), max_value=df.Price.max())
   



#tabs
tab1, tab2, tab3 = st.tabs(["tab1", "tab2", "tab3"])

with tab1:
        #select box
    st.write("You selected:", option)
    filtered_df = filter_transmission(df, option)
    st.dataframe(filtered_df)


    #columns
    col1,col2 = st.columns([2,3])

    with col1:
       with col1:
        # Clean Engine column: remove ' cc' and convert to numeric
        filtered_df['Engine_clean'] = pd.to_numeric(
            filtered_df['Engine'].str.replace(' cc', '', regex=False), 
            errors='coerce'
        )

        # Clean Max Power column: extract the number before 'bhp' and convert to numeric
        filtered_df['MaxPower_clean'] = pd.to_numeric(
            filtered_df['Max Power'].str.extract(r'(\d+\.?\d*)')[0],
            errors='coerce'
        )

        # Drop rows where Engine or Max Power is missing
        df_clean = filtered_df.dropna(subset=['Engine_clean', 'MaxPower_clean'])

        # Plot Engine vs Max Power
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df_clean['Engine_clean'], df_clean['MaxPower_clean'], color='blue', alpha=0.7)
        ax.set_title(f'Engine vs Max Power (Transmission: {option})')
        ax.set_xlabel('Engine (cc)')
        ax.set_ylabel('Max Power (bhp)')
        ax.grid(True)
        st.pyplot(fig)



    with col2:
        st.write("col2")

with tab2:
    #for slider
    st.write("You selected:", price)
    filtered_df = filter_Price(df, price)
    st.dataframe(filtered_df)

    st.divider()

    #range slider
    st.write(start_price,"-",end_price)
    filtered_df = filter_rangePrice(df, start_price,end_price)
    st.dataframe(filtered_df)

    st.divider()

    #for text input
    st.write("You selected:", number_price)
    if number_price:
        filtered_df = filter_Price(df, number_price)
        st.dataframe(filtered_df)

with tab3:
    st.write("TAB3")








