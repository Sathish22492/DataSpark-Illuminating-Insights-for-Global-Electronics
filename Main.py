import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector

# Establish a database connection
db= mysql.connector.connect(
    host="localhost",
    user="root",
    password="nura@29",
    auth_plugin='mysql_native_password',
    database='guvi_capstone')

cursor = db.cursor()
db.commit()
cursor.execute("SELECT * FROM guvi_capstone.customers_details; ")
details1 = cursor.fetchall()
customer = pd.DataFrame(details1, columns=("CustomerKey", "Gender", "Name", "City", "State", "Country","Continent","Birthday","Age"))


cursor = db.cursor()
db.commit()
cursor.execute("SELECT * FROM guvi_capstone.product_details; ")
details2 = cursor.fetchall()
product = pd.DataFrame(details2, columns=("ProductKey", "Product Name", "Brand", "Color", "Unit_Cost_USD", "Unit_Price_USD","Subcategory","CategoryKey","Category"))

cursor = db.cursor()
db.commit()
cursor.execute("SELECT * FROM guvi_capstone.sales_details; ")
details3 = cursor.fetchall()
sales = pd.DataFrame(details3, columns=('Order Number', 'Line Item', 'Order Date', 'Delivery Date', 'CustomerKey', 'StoreKey', 'ProductKey', 'Quantity', 'Currency Code'))

cursor = db.cursor()
db.commit()
cursor.execute("SELECT * FROM guvi_capstone.stores_details; ")
details4 = cursor.fetchall()
stores = pd.DataFrame(details4, columns=('StoreKey', 'Country', 'State', 'Square Meters', 'Open Date'))


def table1(details1):
    query1='''select Country,Count(CustomerKey) as Customers_Count
    from guvi_capstone.Customer_details 
    group by Country 
    order by Customers_Count desc;'''
    cursor.execute(query1)
    data1=cursor.fetchall()

    df1 = pd.DataFrame(data1, columns=["Country", "Customers_Count"])
    col1,col2=st.columns(2)
    with col1:
           df1
    with col2:
        fig1=px.bar(df1, x="Country", y="Customers_Count", title="Customer count vs Country  ", color_discrete_sequence=px.colors.sequential.Pinkyl_r,height=600,width=650)
        st.plotly_chart(fig1)



def table2(details1):
    query2='''SELECT Age, COUNT(CustomerKey) AS Customer_Count
            FROM guvi_capstone.customers_details
            GROUP BY Age
            ORDER BY Customer_Count DESC limit 10;'''
    cursor.execute(query2)
    data1=cursor.fetchall()

    df2 = pd.DataFrame(data1, columns=["Age","Customers_Count"])
    col1,col2=st.columns(2)
    with col1:
           df2
    with col2:
        # Pie chart: Customer Count by Age
        fig2 = px.pie(df2, 
                    values="Customers_Count",  # The size of each slice
                    names="Age",  # Labels for each slice
                    title="Customer Count by Age", 
                    color_discrete_sequence=px.colors.sequential.Pinkyl_r,  # Color scheme
                    height=600, 
                    width=650)

        # Display the pie chart in Streamlit
        st.plotly_chart(fig2)



def table3(details1, details2, details3):
    query3 = '''  
        SELECT c.Country,
               SUM(p.Unit_Price_USD * s.Quantity) - SUM(p.Unit_Cost_USD * s.Quantity) AS total_profit
        FROM 
            guvi_capstone.sales_details AS s
        LEFT JOIN 
            guvi_capstone.product_details AS p
        ON 
            p.ProductKey = s.ProductKey
        LEFT JOIN 
            guvi_capstone.customers_details AS c
        ON 
            s.CustomerKey = c.CustomerKey
        GROUP BY 
            c.Country;'''
    
    cursor.execute(query3)
    data3 = cursor.fetchall()

    # Create a DataFrame with Country and total_profit columns
    df3 = pd.DataFrame(data3, columns=["Country", "Total_Profit"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df3)  # Display the DataFrame in the first column
    
    with col2:
        # Scatter Geo Map: Total Profit by Country
        fig3 = px.scatter_geo(df3, 
                              locations="Country",  # Country names for mapping
                              locationmode="country names",  # Set location mode to country names
                              size="Total_Profit",  # Size of the markers based on total profit
                              hover_name="Country",  # Display country name on hover
                              color="Total_Profit",  # Color of the markers based on total profit
                              color_continuous_scale=px.colors.sequential.Pinkyl_r,  # Color scheme
                              title="Total Profit by Country",
                              height=600, 
                              width=650)
        
        # Display the scatter map in Streamlit
        st.plotly_chart(fig3)

def table4(details1, details2):
    query4 = '''  
        SELECT a.Age, COUNT(b.ProductKey) AS Product_Count
        FROM guvi_capstone.customers_details AS a
        RIGHT JOIN guvi_capstone.sales_details AS b
        ON a.CustomerKey = b.CustomerKey
        GROUP BY a.Age
        ORDER BY Product_Count DESC 
        LIMIT 10;'''
    
    cursor.execute(query4)
    data3 = cursor.fetchall()

    # Create a DataFrame with Age and Product_Count columns
    df4 = pd.DataFrame(data3, columns=["Age", "Product_Count"])
    
    
    st.dataframe(df4)  # Display the DataFrame on the left side

def table5(details1, details2,details3):
    query5 = '''  
        SELECT c.Category, COUNT(b.ProductKey) AS ProductCount
FROM guvi_capstone.customers_details AS a
RIGHT JOIN guvi_capstone.sales_details AS b
ON a.CustomerKey = b.CustomerKey
LEFT JOIN guvi_capstone.product_details AS c
ON b.ProductKey = c.ProductKey  
GROUP BY c.Category
ORDER BY c.Category;'''
    
    cursor.execute(query5)
    data5 = cursor.fetchall()

    # Create a DataFrame with Age and Product_Count columns
    df5= pd.DataFrame(data5, columns=["Category", "ProductCount"])
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(df5)  # Display the DataFrame on the left side

    with col2:
        fig5=px.bar(df5, x="Category", y="ProductCount", title="category vs product count  ", color_discrete_sequence=px.colors.sequential.Pinkyl_r,height=600,width=650)
        st.plotly_chart(fig5)


def table6(details1, details2,details3):
    query6 = '''  
SELECT 
    p.Product_Name,
    SUM(p.Unit_Price_USD * (s.Quantity)) AS total_revenue
FROM 
    guvi_capstone.sales_details AS s
LEFT JOIN 
    guvi_capstone.product_details AS p
ON 
    p.ProductKey = s.ProductKey
GROUP BY 
    p.ProductKey,
    p.Product_Name

ORDER BY 
    total_revenue DESC limit 10;;
;'''
    
    cursor.execute(query6)
    data6 = cursor.fetchall()

    # Create a DataFrame with Age and Product_Count columns
    df6= pd.DataFrame(data6, columns=["Product Name", "Total Revenue"])
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(df6)  # Display the DataFrame on the left side

    with col2:
        fig6=px.bar(df6, x="Total Revenue", y="Product Name", title="Top 10 revenued product", color_discrete_sequence=px.colors.sequential.Bluered_r,height=600,width=650,orientation="h")
        st.plotly_chart(fig6)



def table7( details2,details3):
    query7 = '''  
SELECT 
    p.Product_Name,
    p.Unit_Cost_USD
FROM 
    guvi_capstone.product_details AS p
LEFT JOIN 
    guvi_capstone.sales_details AS s
ON 
    p.ProductKey = s.ProductKey
GROUP BY 
    p.ProductKey,
    p.Product_Name,
    p.Unit_Cost_USD
HAVING 
    SUM(COALESCE(s.Quantity, 0)) = 0
ORDER BY 
    p.Unit_Cost_USD DESC limit 10;
;'''
    
    cursor.execute(query7)
    data7 = cursor.fetchall()

    # Create a DataFrame with Age and Product_Count columns
    df7= pd.DataFrame(data7, columns=["Product Name", "Total Cost"])
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(df7)  # Display the DataFrame on the left side

    with col2:
        fig7=px.bar(df7, x="Total Cost", y="Product Name", title="Top 10 Products not sold", color_discrete_sequence=px.colors.sequential.Bluered_r,height=600,width=650,orientation="h")
        st.plotly_chart(fig7)


def table8( details2,details3):
    query8 = '''  
SELECT 
    p.Brand,
    SUM(p.Unit_Price_USD * (s.Quantity))-SUM(p.Unit_Cost_USD * (s.Quantity)) AS total_profit
FROM 
    guvi_capstone.sales_details AS s
LEFT JOIN 
    guvi_capstone.product_details AS p
ON 
    p.ProductKey = s.ProductKey

GROUP BY 
P.Brand

ORDER BY 
    total_profit
 DESC ;'''
    
    cursor.execute(query8)
    data8 = cursor.fetchall()

    # Create a DataFrame with Age and Product_Count columns
    df8= pd.DataFrame(data8, columns=["Brand", "Total Profit"])
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(df8)  # Display the DataFrame on the left side

    with col2:
        fig8=px.bar(df8, x="Brand", y="Total Profit", title="Brand vs Profit", color_discrete_sequence=px.colors.sequential.Agsunset,height=600,width=650)
        st.plotly_chart(fig8)


def table9(details2, details3, details4):
    query9 = '''  
    SELECT 
        t.Country, 
        t.State, 
        SUM(p.Unit_Price_USD * s.Quantity) AS total_revenue
    FROM 
        guvi_capstone.sales_details AS s
    LEFT JOIN 
        guvi_capstone.product_details AS p
    ON 
        p.ProductKey = s.ProductKey
    LEFT JOIN 
        guvi_capstone.stores_details AS t
    ON 
        s.StoreKey = t.StoreKey
    WHERE 
        t.StoreKey IS NOT NULL
    GROUP BY 
        t.Country, t.State
    ORDER BY 
        total_revenue DESC;
    '''
    
    # Execute the query and fetch the results
    cursor.execute(query9)
    data9 = cursor.fetchall()

    # Create a DataFrame with Country, State, and Total Revenue columns
    df9 = pd.DataFrame(data9, columns=["Country", "State", "Total Revenue"])

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df9)  # Display the DataFrame on the left side

    with col2:
       
        # Create scatter geo map showing states in multiple countries
        fig9 = px.scatter_geo(df9,
                            locations="Country",  
                            locationmode="country names",  
                            size="Total Revenue",  
                            hover_name="Country", 
                            color="Total Revenue",
                            hover_data={"Country": True},  
                            color_continuous_scale=px.colors.sequential.Pinkyl_r,  
                            title="Total Revenue by State in Different Countries",
                            height=600,
                            width=650,
                            scope="world")  # Set scope to world for all countries

        # Display the scatter map in Streamlit
        st.plotly_chart(fig9)








# Set the layout for the Streamlit app
st.set_page_config(layout="wide")
# Display the main title
st.markdown("<h1 style='display: flex; align-items: center; font-size: 27px; margin: 0;'>DATASPARK INSIGHTS</h1>", unsafe_allow_html=True)
st.write("To know more search for different question given below:")

Question = st.selectbox("select your question",[
        "1. which is country has high customers?",
        "2. customer age distribution over the country",
        "3. profit distribution over the country",
        "4. whcih age category of the customer purchased more",
        "5. category vs product sold",
        "6. Top 10 revenued product",
        "7. Top 10 cost of products which are not sold",
        "8. Brand wise Total Profit",
        "9. store performance based on sales"])



if Question=="1. which is country has high customers?":
   table1(customer)


elif Question=="2. customer age distribution over the country":
   table2(customer)

elif Question=="3. profit distribution over the country":
   table3(customer,product,sales)

elif Question=="4. whcih age category of the customer purchased more":
   table4(customer,product)
       
elif Question=="5. category vs product sold":
   table5(customer,product,sales)
       
elif Question=="6. Top 10 revenued product":
   table6(customer,product,sales)

elif Question=="7. Top 10 cost of products which are not sold":
   table7(product,sales)
             
elif Question=="8. Brand wise Total Profit":
   table8(product,sales)
             
elif Question=="9. store performance based on sales":
   table9(product,sales,stores)
