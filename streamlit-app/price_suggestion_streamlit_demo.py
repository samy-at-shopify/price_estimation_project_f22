import json
import requests
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
plt.style.use('seaborn')
from streamlit_modal import Modal
import streamlit.components.v1 as components

product_title = ""
product_category = ""
vendor = ""
tag_string = ""
fulfillment_service = ""

def get_price_suggestion():
  global product_title
  global product_category
  global vendor
  global tag_string
  global fulfillment_service

  d = dict(
    product_title = product_title,
    product_category = product_category,
    vendor = vendor,
    tag_string = tag_string,
    fulfillment_service = fulfillment_service
  )
  print(d)

  r = requests.post(
    "https://25988c0885db42d9afeb4cdca53b5f3d.changeme.shopifynetwork.com/suggest",
    auth = ('DEMO_ACCOUNT', 'I08S0wOOn8yBirtvfusHpm8vraJoqTcq'),
    headers={
      'Authorization': 'Basic REVNT19BQ0NPVU5UOkkwOFMwd09Pbjh5QmlydHZmdXNIcG04dnJhSm9xVGNx',
      'Content-Type': 'application/json',
      'Cookie': 'MINERVA_TOKEN=eyJraWQiOiIzM2QyNDNhZmNkOTVjNzY4ZjQ5OTMzZGJlM2ZkMDVjN2ViMzY3YzVkYTUzNDIxOThlMjA2NGIxYmViMTk5NzczIiwiYWxnIjoiUlMyNTYifQ.eyJyZXF1ZXN0X2lkIjoiZjYyNDMwOTEtYjBlZC00MTcyLWExYjEtNjk1YmNiNGQxYzNlIiwiYWNjZXNzZWRfc2hvcHMiOnt9LCJhdWQiOiIyNTk4OGMwODg1ZGI0MmQ5YWZlYjRjZGNhNTNiNWYzZC5jaGFuZ2VtZS5zaG9waWZ5bmV0d29yay5jb20iLCJlbWFpbCI6InNhbXkuY291bG9tYmVAc2hvcGlmeS5jb20iLCJlbXBsb3llZV9pZCI6MjI5OTAsImV4cCI6MTY3MDI2ODUxOSwiZXh0cmEiOm51bGwsImZpcnN0X25hbWUiOiJTYW15IiwiaWF0IjoxNjcwMTgyMTE5LCJpZCI6IjRjYmJmMjcwLTExMjUtNDk3OS1iMDY0LTIyNDExYTIzMDM1ZSIsImlwIjoiOC4yOS4yMzAuMzQiLCJpc3MiOiJNaW5lcnZhIiwibGFzdF9uYW1lIjoiQ291bG9tYmUiLCJwZXJtaXNzaW9ucyI6bnVsbCwicmVxdWlyZW1lbnRzIjpbImF1dGhlbnRpY2F0ZWRfZGV2aWNlPyIsImF1dGhvcml6ZWRfZm9yX3VzZXJfcm9sZT8iLCJjaGVja19jaHJvbWVib29rIiwiZG9uZV90cmFpbmluZz8iLCJldmFsdWF0ZV9wcm9wb3NlZF9yYmFjX3VwZGF0ZXMiLCJtYW5hZ2VkX21hYz8iLCJyZXF1aXJlX21hbmFnZWRfYnJvd3Nlcj8iLCJzYW1lX2RldmljZT8iLCJzZWN1cmVfaW9zIiwic2VjdXJlX21hY29zPyIsInNvZnRibG9ja2VkX2Jwbz8iLCJ0cnVzdGVkX2Ruc19jaHJvbWVib29rPyIsInRydXN0ZWRfZG5zX21hYz8iLCJ1c2VyX2FjY2Vzc19yZXN0cmljdGVkPyIsInZhbGlkX3VzZXJfY2VydGlmaWNhdGVfdXNhZ2U_Il0sInNob3Bfc2x1Z3NfdG9faWRzIjp7fX0.JWeJWSpj1nvLXKndyqlR45UGR2CV38Yk8WlWxrvsQh3k8NtHRqB4zyty1tCmaVpeABxol1va8C1t7mT4FCxpuZC60gqpUAeUgHEBDAcBQvyDs1Dlb0lUZ33GDcyxSeEVkPhB2N5JzRkdUXcNddHXN2NVQxferosaIpXUn9Tn7EPvK03AFwiTwxlrZ2f8Cxc9U7d_zrDS-INn7tkjjQmqRosJufBVcS9ucDcwEomZv-Gk9djXGfgmK7rfv2tkZY8NLVrZQiQG05LXOSPvlLw9PqGk8Ju2PBmb2OLMYgeoGVxoqqyCbii0sMGo6-2SaXgi6MUi-_WbHLZlM11XjcS51w'
    },
    json = {
      "product_category": product_category,
      "fulfillment_service": fulfillment_service,
      "vendor": vendor,
      "product_title": product_title,
      "variant_title": "",
      "tag_string": tag_string,
      "options": ""
    }
  )
  return r.status_code, r.text

st.image("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjMwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yMS40OCA2LjEwMWEuMjUzLjI1MyAwIDAgMC0uMjQtLjIyYy0uMSAwLTIuMDgtLjA0LTIuMDgtLjA0cy0xLjY2LTEuNi0xLjgyLTEuNzhjLS4xNi0uMTYtLjQ4LS4xMi0uNi0uMDhsLS44NC4yNmMtLjA4LS4yOC0uMjItLjYyLS40LS45OC0uNTgtMS4xMi0xLjQ2LTEuNzItMi41LTEuNzItLjA4IDAtLjE0IDAtLjIyLjAyLS4wNC0uMDQtLjA2LS4wOC0uMS0uMS0uNDYtLjQ4LTEuMDQtLjcyLTEuNzQtLjctMS4zNC4wNC0yLjY4IDEuMDItMy43OCAyLjc0LS43NiAxLjIyLTEuMzQgMi43NC0xLjUyIDMuOTItMS41NC40OC0yLjYyLjgyLTIuNjYuODItLjc4LjI0LS44LjI2LS45IDEtLjA0LjU2LTIuMDggMTYuMzQtMi4wOCAxNi4zNGwxNy4xMiAyLjk2IDcuNDItMS44NGMtLjAyIDAtMy4wNC0yMC40Ni0zLjA2LTIwLjZabS02LjQ0LTEuNThjLS40LjEyLS44NC4yNi0xLjMyLjQyIDAtLjY4LS4xLTEuNjQtLjQtMi40NCAxLjAyLjE2IDEuNTIgMS4zMiAxLjcyIDIuMDJabS0yLjIyLjY4Yy0uOS4yOC0xLjg4LjU4LTIuODYuODguMjgtMS4wNi44LTIuMSAxLjQ0LTIuOC4yNC0uMjYuNTgtLjU0Ljk2LS43LjQuNzguNDggMS44OC40NiAyLjYyWm0tMS44NC0zLjU0Yy4zMiAwIC41OC4wNi44LjIyLS4zNi4xOC0uNzIuNDYtMS4wNC44Mi0uODYuOTItMS41MiAyLjM0LTEuNzggMy43Mi0uODIuMjYtMS42Mi41LTIuMzQuNzIuNDgtMi4xOCAyLjMtNS40MiA0LjM2LTUuNDhaIiBmaWxsPSIjOTVCRjQ3Ii8+PHBhdGggZD0iTTIxLjI0IDUuODgxYy0uMSAwLTIuMDgtLjA0LTIuMDgtLjA0cy0xLjY2LTEuNi0xLjgyLTEuNzhhLjMyMS4zMjEgMCAwIDAtLjIyLS4xdjI0LjU4bDcuNDItMS44NC0zLjA0LTIwLjZjLS4wNC0uMTQtLjE2LS4yMi0uMjYtLjIyWiIgZmlsbD0iIzVFOEUzRSIvPjxwYXRoIGQ9Im0xMyA5LjcwMS0uODYgMy4yMnMtLjk2LS40NC0yLjEtLjM2Yy0xLjY4LjEtMS42OCAxLjE2LTEuNjggMS40Mi4xIDEuNDQgMy44OCAxLjc2IDQuMSA1LjE0LjE2IDIuNjYtMS40IDQuNDgtMy42OCA0LjYyLTIuNzIuMTQtNC4yMi0xLjQ2LTQuMjItMS40NmwuNTgtMi40NnMxLjUyIDEuMTQgMi43MiAxLjA2Yy43OC0uMDQgMS4wOC0uNyAxLjA0LTEuMTQtLjEyLTEuODgtMy4yLTEuNzYtMy40LTQuODYtLjE2LTIuNiAxLjU0LTUuMjIgNS4zLTUuNDYgMS40Ni0uMSAyLjIuMjggMi4yLjI4WiIgZmlsbD0iI2ZmZiIvPjxwYXRoIGQ9Ik0zNC41OCAxNi41NjFjLS44Ni0uNDYtMS4zLS44Ni0xLjMtMS40IDAtLjY4LjYyLTEuMTIgMS41OC0xLjEyIDEuMTIgMCAyLjEyLjQ2IDIuMTIuNDZsLjc4LTIuNHMtLjcyLS41Ni0yLjg0LS41NmMtMi45NiAwLTUuMDIgMS43LTUuMDIgNC4wOCAwIDEuMzYuOTYgMi4zOCAyLjI0IDMuMTIgMS4wNC41OCAxLjQgMSAxLjQgMS42MiAwIC42NC0uNTIgMS4xNi0xLjQ4IDEuMTYtMS40MiAwLTIuNzgtLjc0LTIuNzgtLjc0bC0uODQgMi40czEuMjQuODQgMy4zNC44NGMzLjA0IDAgNS4yNC0xLjUgNS4yNC00LjItLjAyLTEuNDYtMS4xMi0yLjUtMi40NC0zLjI2Wk00Ni43IDExLjUwMWMtMS41IDAtMi42OC43Mi0zLjU4IDEuOGwtLjA0LS4wMiAxLjMtNi44SDQxbC0zLjMgMTcuMzJoMy4zOGwxLjEyLTUuOTJjLjQ0LTIuMjQgMS42LTMuNjIgMi42OC0zLjYyLjc2IDAgMS4wNi41MiAxLjA2IDEuMjYgMCAuNDYtLjA0IDEuMDQtLjE0IDEuNWwtMS4yOCA2Ljc4aDMuMzhsMS4zMi03Yy4xNC0uNzQuMjQtMS42Mi4yNC0yLjIyLjAyLTEuOTItLjk4LTMuMDgtMi43Ni0zLjA4Wk01Ny4xNCAxMS41MDFjLTQuMDggMC02Ljc4IDMuNjgtNi43OCA3Ljc4IDAgMi42MiAxLjYyIDQuNzQgNC42NiA0Ljc0IDQgMCA2LjctMy41OCA2LjctNy43OC4wMi0yLjQyLTEuNC00Ljc0LTQuNTgtNC43NFptLTEuNjYgOS45NGMtMS4xNiAwLTEuNjQtLjk4LTEuNjQtMi4yMiAwLTEuOTQgMS01LjEgMi44NC01LjEgMS4yIDAgMS42IDEuMDQgMS42IDIuMDQgMCAyLjA4LTEuMDIgNS4yOC0yLjggNS4yOFpNNzAuNCAxMS41MDFjLTIuMjggMC0zLjU4IDIuMDItMy41OCAyLjAyaC0uMDRsLjItMS44MmgtM2MtLjE0IDEuMjItLjQyIDMuMS0uNjggNC41bC0yLjM2IDEyLjRoMy4zOGwuOTQtNS4wMmguMDhzLjcuNDQgMS45OC40NGMzLjk4IDAgNi41OC00LjA4IDYuNTgtOC4yIDAtMi4yOC0xLjAyLTQuMzItMy41LTQuMzJabS0zLjI0IDkuOThjLS44OCAwLTEuNC0uNS0xLjQtLjVsLjU2LTMuMTZjLjQtMi4xMiAxLjUtMy41MiAyLjY4LTMuNTIgMS4wNCAwIDEuMzYuOTYgMS4zNiAxLjg2IDAgMi4yLTEuMyA1LjMyLTMuMiA1LjMyWk03OC43NCA2LjY0MWMtMS4wOCAwLTEuOTQuODYtMS45NCAxLjk2IDAgMSAuNjQgMS43IDEuNiAxLjdoLjA0YzEuMDYgMCAxLjk2LS43MiAxLjk4LTEuOTYgMC0uOTgtLjY2LTEuNy0xLjY4LTEuN1pNNzQgMjMuNzgxaDMuMzhsMi4zLTEyaC0zLjRsLTIuMjggMTJaTTg4LjMgMTEuNzYxaC0yLjM2bC4xMi0uNTZjLjItMS4xNi44OC0yLjE4IDIuMDItMi4xOC42IDAgMS4wOC4xOCAxLjA4LjE4bC42Ni0yLjY2cy0uNTgtLjMtMS44NC0uM2MtMS4yIDAtMi40LjM0LTMuMzIgMS4xMi0xLjE2Ljk4LTEuNyAyLjQtMS45NiAzLjg0bC0uMS41NmgtMS41OGwtLjUgMi41NmgxLjU4bC0xLjggOS40OGgzLjM4bDEuOC05LjQ4aDIuMzRsLjQ4LTIuNTZaTTk2LjQ2IDExLjc4MXMtMi4xMiA1LjM0LTMuMDYgOC4yNmgtLjA0Yy0uMDYtLjk0LS44NC04LjI2LS44NC04LjI2aC0zLjU2TDkxIDIyLjgwMWMuMDQuMjQuMDIuNC0uMDguNTYtLjQuNzYtMS4wNiAxLjUtMS44NCAyLjA0LS42NC40Ni0xLjM2Ljc2LTEuOTIuOTZsLjk0IDIuODhjLjY4LS4xNCAyLjEyLS43MiAzLjMyLTEuODQgMS41NC0xLjQ0IDIuOTgtMy42OCA0LjQ0LTYuNzJsNC4xNC04LjloLTMuNTRaIiBmaWxsPSIjMDAwIi8+PC9zdmc+")
st.title('Price Suggestion Demo')


st.header('Add product')
left_column, right_column = st.columns([3,2])
with left_column:
  product_title = st.text_input('Product title', placeholder='T-shirt')

  product_description = st.text_area('Product description')

  st.subheader('Media')
  uploaded_file = st.file_uploader("Upload media")

  st.subheader('Pricing')
  price = st.text_input('Price ($)', placeholder='0.00')
  compare_at_price = st.text_input('Compare at price ($)', placeholder='0.00')
  st.checkbox('Charge tax on this product')
  cost_per_item = st.text_input('Cost per item ($)', placeholder='0.00')
  st.caption("Customers won't see this")

  st.subheader('Inventory')
  st.text_input('SKU (Stock Keeping Unit)')
  st.text_input('Barcode (ISBN, UPC, GTIN, etc.)')
  st.checkbox('Track quantity')
  st.checkbox('Continue selling when out of stock')

  st.subheader('Shipping')
  st.checkbox('This is a physical product')
  st.text('WEIGHT')
  st.caption('Used to calculate shipping rates at checkout and label prices during fulfillment. See guidelines for estimating product weight.')
  st.text_input('Weight')
  st.selectbox('', ['kg','lb'])

  fulfillment_service = st.text_input('Fulfillment service')

  st.text('CUSTOMS INFORMATION')
  st.caption('Customs authorities use this information to calculate duties when shipping internationally. Shown on printed customs forms.')
  st.selectbox('Country/Region of origin', ['Canada'])
  st.caption('In most cases, where the product is manufactured.')
  st.text_input('HS (Harmonized System) code', placeholder='Search or enter a HA code')
  st.caption('Manually enter codes that are longer than 6 numbers.')

  st.subheader('Options')
  st.checkbox('This product has options, like size or color')

with right_column:
  st.subheader('Product status')
  st.selectbox('', ['Active', 'Draft'])
  st.caption('This product will be available to 1 sales channel.')
  st.text('SALES CHANNELS AND APPS')
  st.checkbox('Online Store')

  st.subheader('Product organization')
  product_category = st.text_input('Type')
  vendor = st.text_input('Vendor')
  st.text_input('Collections')
  tag_string = st.text_input('Tags', placeholder = 'first, second, third')

  with st.expander("Price suggestion?"):
    if st.button("Launch price suggestion!"):
      status_code, response_body = get_price_suggestion()
      response_body = json.loads(response_body)
      print(status_code)
      suggestion = response_body['suggested_price']
      low, high = response_body['suggestion_range']
      data = response_body['similar_product_prices']
      st.markdown(f"We suggest **${suggestion}**, but anywhere from **{low}** to **{high}** would make sense 😃")
      fig, ax = plt.subplots(figsize=(6, 4))
      sns.histplot(data, ax=ax, bins=100, kde=True, element="step")
      ax.axvline(x=suggestion)
      ax.fill_betweenx([0], [low], x2=[high])
      ax.set_ylabel("Frequency")
      ax.set_xlabel("Price ($)")
      st.pyplot(fig)
