

#Imports Streamlit and Matplotlib naming them st and plt respectively
import streamlit as st
import matplotlib as plt

margin_of_safety_units = 17
max_units = 1517

st.write("Margin of Safety Units:", margin_of_safety_units)
st.write("10% of Max Units:", max_units * 0.1)

if margin_of_safety_units < 0:
    st.warning("⚠️ Your units range is below break-even, meaning the business is operating at a loss.")
elif margin_of_safety_units < max_units * 0.1:
    st.warning("⚠️ Margin of safety is low — sales can easily fall below break-even.")
else:
    st.success("✅ Margin of safety is healthy.")


