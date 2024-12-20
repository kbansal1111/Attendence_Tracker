import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import os
import google.generativeai as ggi


st.title('AI Expense Tracker')
st.info('This AI model will help u your finance')
user_name=st.text_input('enter your name')
st.write()
monthly_income=st.number_input('your monthly income')
st.write()
savings=st.number_input('monthly savings')
st.write()
product_category = st.selectbox(
    "Select your Category",
    options=["Food", "Travel", "Entertainment", "Bills", "Others"]
)
product_amount = st.number_input("Enter the Amount", min_value=0, step=1)

if "expense" not in st.session_state:
    st.session_state["expense"] = pd.DataFrame(columns=["Name", "monthly income", "product category", "product amount","savings"])
    
if st.button("Add Expenditure"):
    if user_name and product_amount>0:
        entry=pd.DataFrame([{'Name':user_name,'monthly income':monthly_income,'product category':product_category,'product amount':product_amount,'savings':savings}])
        st.session_state["expense"]=pd.concat([st.session_state["expense"], entry])
        st.success("Expenditure added successfully")
    else:
        st.error("please fill entry correctly")
if not st.session_state["expense"].empty:
    st.header("your expenditure")
    st.dataframe(st.session_state["expense"])
total_amount_spend=st.session_state["expense"]["product amount"].sum()
st.write(f"Total expenditure is {total_amount_spend}")

# Graph
fig,ax = plt.subplots(figsize=(3,3))
ax.bar(['monthly income', 'Total Expenditure'], [monthly_income, total_amount_spend], color=['green', 'red'])
ax.set_ylabel('Amount')
ax.set_title('Monthly Income vs Total Expenditure')
st.pyplot(fig)

# model using gemini api
def format_expenses(expense, monthly_income, total_amount_spend):
    expense_summary = f"User's monthly income: {monthly_income}\n"
    expense_summary += f"Total expenditure: {total_amount_spend}\n"
    expense_summary += "Breakdown of expenses by category:\n"

    for _, row in expense.iterrows():
        expense_summary += f"- {row['product category']}: {row['product amount']} (Savings: {row['savings']})\n"

    remaining_income = monthly_income - total_amount_spend
    expense_summary += f"\nRemaining income: {remaining_income}\n"
    
    return expense_summary

API_KEY="AIzaSyCFZy1n4bvWj3QXAC1nrwJr5aPQl43H2_k"
ggi.configure(api_key=API_KEY)
model = ggi.GenerativeModel("gemini-pro") 
chat = model.start_chat()

def LLM_Response(question):
    response = chat.send_message(question,stream=True)
    return response

st.write("Financial advices")
btn = st.button("Ask")

if btn:
    expense_details = format_expenses(st.session_state["expense"], monthly_income, total_amount_spend)
    prompt = f"Here are the user's income, savings, and expenses. Please provide financial advice based on this:\n{expense_details}\nUser's question: {user_name}, {product_category}, {product_amount}"
    
    result = LLM_Response(prompt)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)
