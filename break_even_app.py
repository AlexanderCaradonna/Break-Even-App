# Imports Streamlit and Matplotlib naming them st and plt respectively
import streamlit as st 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sets the main title of the web app
st.title("📋 Break-Even Analysis App")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧾 Business Inputs", "📊 Financial Metrics", "📉 Break-even Analysis", "📈 Forecast & Charts", "⚖️ Sensitivity Analysis"])

# User inputs for fixed cost, price per unit, and variable cost per unit
with tab1:
    
    st.header("Inputs")
    fixed_costs = st.number_input("Enter fixed costs ($)", min_value=0.0, value=3000.0)             # Creates input box for user and stores value entered in fixed_costs
    variable_cost = st.number_input("Enter variable cost per unit ($)", min_value=0.0, value=10.0)  # Creates .... and stores value entererd in variable_cost
    price_per_unit = st.number_input("Enter price per unit ($)", min_value=0.01, value=25.0)        # Creates .... and stores value in price_per_unit
    sales = st.number_input("Enter estimated sales per month (Units)", min_value=1.0, value=200.0)
    max_units = st.slider("Units range to analyze", 0, 10000, 500)                                   # Creates a slider input to let the user select their number of units, stored in max_units
    st.session_state['estimatedSales'] = sales                                                      # Stores the sales variable into a state called "estimatedSales", lets us use this state later on
    
    # Declaring Variables
    cm_ratio = (price_per_unit - variable_cost) / price_per_unit
    contribution_margin_per_unit = price_per_unit - variable_cost
    estimated_rev = price_per_unit * sales
    total_revenue = price_per_unit * max_units                                                      # Revenue formula
    profit_at_max_units = (max_units * price_per_unit) - (fixed_costs + variable_cost * max_units)  # Profit = Revenue - Total Costs
    operating_profit_margin = profit_at_max_units / total_revenue if total_revenue != 0 else 0      # Does the calculation if total revenue is not equal to 0, " !=0 " means not equal to 0
    break_even_units = fixed_costs / (price_per_unit - variable_cost) if contribution_margin_per_unit !=0 else 0
    break_even_revenue = break_even_units * price_per_unit
    payback_period = break_even_units / sales
    margin_of_safety_units = max_units - break_even_units                                           # MOS formula
    margin_of_safety_revenue = margin_of_safety_units * price_per_unit                              # MOSR formula


    if max_units < sales:
            st.warning(f"⚠️ Your analysis range ({max_units}) is smaller than your estimated monthly sales ({sales:.0f} Units). "
                       "Consider increasing the units range to get a full picture of monthly sales and profits")
           
    if price_per_unit <= variable_cost:
        st.error("⚠️ Price per unit must be greater than variable cost.")

 
with tab2:    

    st.header("Financial Key Metrics")

    # Break-even calculation
    if price_per_unit > variable_cost:

        # st.write is to output information
        st.write(f"•  **Break-Even Units**: {break_even_units:.0f}")        # Displays break even units with 2 decimal places
        st.write(f"•  **Break-Even Revenue**: ${break_even_revenue:,.2f}")  # Displays break even units with 2 decimal places and "," as thousand separator
        st.write(f"•  **Contribution Margin per Unit:** {contribution_margin_per_unit:.2f}")
        st.write(f"•  **Contribution Margin Ratio**: {cm_ratio:.2%}")
        st.write(f"•  **Estimated monthly revenue is:** ${estimated_rev:,.2f}")
        st.write(f"•  **Operating Profit Margin at {max_units} units:** {operating_profit_margin:.2%}")
        st.write(f"•  **Estimated Time to Break Even:** {payback_period:.1f} months")
            
        if break_even_units > max_units:                                                        # Checks if BE units exceed units user selected (max_units)
            st.warning(
                f"🚨 Warning: Break-even point ({break_even_units:.0f} units) "                 # Sends warning message that BEP too high, i.e not in range
                f"is beyond your analysis range ({max_units} units). "
                "Consider increasing price, reducing costs, or increasing sales volume.")
        else:
            st.success(
                f"✅ You will break even after selling approximately {break_even_units:.0f} units. "    # Sends success message that successfully BE at BE units
                "Sales beyond this will generate profit.")
    else:
        st.error("⚠️ Price per unit must be greater than variable cost.")   # Error message displayed if price_per_unit < variable_cost    


with tab3:

    st.header("Break Even Analysis")

    if price_per_unit > variable_cost:

        st.write(f"• **Margin of Safety:** {margin_of_safety_units:.0f} units")              # Displays MOS units
        st.write(f"• **Margin of Safety Revenue:** ${margin_of_safety_revenue:,.2f}")        # Displays MOSR   
        st.write(f"• **Profit at {max_units} units sold:** ${profit_at_max_units:,.2f}")     # Displays profit at {units user selected} sold with $ amount

        # Commentary on margin of safety
        if profit_at_max_units > 0:                                                                                 # To calculate operating leverage only if in profit
            contribution_margin = (price_per_unit - variable_cost) * max_units                                      # CM formula
            dol = contribution_margin / profit_at_max_units                                                         # Operating leverage formula
            st.write(f"• **Degree of Operating Leverage at {max_units} units:** {dol:.2f}")                       # Output dol and operating leverage at units

            if dol > 5:
                st.warning("⚠️ Operating Leverage Too High - Profits are sensitive to changes in quantity")
            elif dol > 2:
                st.info(" ℹ️ Moderate Operating Leverage")
            else:
                st.success(" ✅ Low Operating Leverage - Profits are relatively stable")
        else:

            st.write("ℹ️ **Operating leverage not calculated because profit is zero or negative**")

        if margin_of_safety_units < 0:
                st.warning("⚠️ Your units range is below break-even, meaning the business is operating at a loss.")     # Warning message when MOS units < 0
        elif margin_of_safety_units < max_units * 0.1:
                st.warning("⚠️ Margin of safety is low — sales can easily fall below break-even.")                      # Warning message when MOS units < 10% of units user selected
        else:                                                                                                    # elif used to check another condition before proceeding to else
                st.success("✅ Margin of safety is healthy. You have a buffer before losses occur.")                    # Success message that MOS is healthy
    

        st.subheader("Insights & Recommendations")

        # Recommendation based on break-even point
        if break_even_units > max_units:                # To check if break even units exceed units user selected
            st.write("🔸 Your break-even point is higher than your expected sales. Consider lowering fixed or variable costs, or increasing price.")
        else:
            st.write("✅ You're expected to reach break-even within your sales range — good job!")

        # Recommendation based on profit
        if profit_at_max_units <= 0:            
            st.write("🔸 You're not making a profit at your maximum sales volume. Reassess your pricing or cost structure.")    # Output message if profit <= 0
        elif profit_at_max_units < 0.2 * total_revenue:                                                                         # Check another condition if profit < 20% of revenue
            st.write("🔸 You're making a small profit (less than 20% of revenue). Consider increasing price or reducing costs")
        else:
            st.write("💰 You're making a healthy profit at your current sales volume.")

        # Recommendation based on margin of safety
        if margin_of_safety_units < max_units * 0.1:                                                            # To check if MOS units < units user selected
            st.write("⚠️ Your margin of safety is very small — a small dip in sales could lead to losses.")
        else:
            st.write("🛡️ Your margin of safety is healthy. Your business has a buffer against sales drops.")

    else:
        st.error("⚠️ Price per unit must be greater than variable cost.")


with tab4:

    st.header("Break-Even Chart")
    
    if price_per_unit > variable_cost:
        
        
        # Data for chart
        
        units = list(range(0, max_units + 1))                               # Creates a list from 0 to max units selected by user
        total_costs = [fixed_costs + variable_cost * u for u in units]      # Calculates costs for each unit level using for loop
        revenue = [price_per_unit * u for u in units]                       # Calculates total revenue for each unit level using for loop
        
        # Plot chart
        fig, ax = plt.subplots()                                                                                    # Creates Matplotlib figure and axes for plotting
        ax.plot(units, revenue, label='Revenue', color='green')                                                     # Plots revenue line
        ax.plot(units, total_costs, label='Total Cost', color='red')                                                # Plots total cost line
        ax.plot(break_even_units, break_even_revenue, 'o', color='blue', markersize=5, label='Break-Even Point')    # Adds a blue dot to break even point
        ax.plot([0, max_units], [fixed_costs, fixed_costs], label='Fixed Costs', color='purple', linestyle='--')    # Plots horizontal line for fixed costs
        ax.set_xlim(0, max_units)                                                                                   # Set x axis limits from 0 to max_units
        ax.set_ylim(0, max(max(total_costs), max(revenue)) * 1.1)                                                   # Set y axis limits from 0 to 110% of max cost/revenue value
        ax.set_xlabel('Units Sold')
        ax.set_ylabel('Dollars ($)')
        ax.set_title('Break-Even Analysis Chart')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        df_break_even = pd.DataFrame({              # Creates data frame containing 3 columns: Units, TC, Revenue
        'Units': units,
        'Total Costs': total_costs,
        'Revenue': revenue})

        csv = df_break_even.to_csv(index=False)     # Converts the dataframe into csv format

        st.download_button(                         # Displays download button
        label="Download Break-Even Data as CSV",
        data=csv,                                   # Tells streamlit what file content to include in the download
        file_name='break_even_data.csv',
        mime='text/csv')                            # Tells the browser to treat it as a text file with csv content
        

        st.header("Profitability Metrics Comparison")

        metrics_labels = ['Contribution Margin', 'Operating Profit']                                # Created variable to hold two name labels for bar chart
        metrics_values = [contribution_margin_per_unit, operating_profit_margin * price_per_unit]   # Stores the actual numbers corresponding to the labels

        fig2, ax2 = plt.subplots()                                                                  # fig2 is the foundation, the piece of paper that the graph will be drawn on, ax2 is the graph that will be drawn/displayed on this paper
        bars = ax2.bar(metrics_labels, metrics_values, color=['skyblue', 'orange'])                 # Assinged to "bars" to keep reference of each individual bar. bars contains list of each individual bar in chart
        ax2.set_ylabel('Dollars ($)')
        ax2.set_title('Unit Profitability Comparison')

        # Annotate bars
        for bar in bars:                                                                        # for loop to go through each individual bar in the bar chart
            height = bar.get_height()                                                           # Finds the height of that one bar and stores it in the variable "height"
            ax2.annotate(f'${height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),      # To put the dollar amount label right above the center of each bar in the bar chart
                     xytext=(0, 1), textcoords="offset points", ha='center', va='bottom')       

        st.pyplot(fig2)

        st.caption("""
        🔹 **Contribution Margin per Unit** is the amount each unit contributes to covering fixed costs and generating profit.  
        🔸 **Operating Profit per Unit** shows the dollar amount retained after covering variable and fixed operating costs.
        """)


        st.header("Sales & Profit Forecast")

        default_sales = st.session_state.get('estimatedSales',0)            # Looks in session state if any data in state called "estimatedSales", if exists it stores it in default_sales, if does not exist 0 will output
        default_sales = int(default_sales)                                  # Converts value to integer

        forecast_months = st.number_input("Forecast Period (Months)", min_value=1, max_value=24, value=12)
        growth_rate = st.number_input("Monthly Sales Growth Rate (%)", min_value=-100.0, max_value=100.0, value=5.0)
        starting_sales = st.number_input("Estimated Monthly Sales (Units)", min_value=0, value=default_sales)           # Side note: needed to convert default_sales to integer before it could be used here because number.input cant accept string
        
        st.markdown('<p style="font-size:12px; font-style:italic; color:gray; margin-top:-15px; margin-bottom:2px;"> Estimated sales is taken from Business Inputs by default</p>', unsafe_allow_html=True)

        forecast_sales = [starting_sales * ((1 + growth_rate / 100) ** month) for month in range(forecast_months)]
        forecast_profit = [(price_per_unit - variable_cost) * s - fixed_costs for s in forecast_sales]

        fig4, ax = plt.subplots()
        ax.plot(range(1, forecast_months + 1), forecast_sales, label="Forecasted Sales")
        ax.plot(range(1, forecast_months + 1), forecast_profit, label="Forecasted Profit")
        ax.set_xlabel("Month")
        ax.set_ylabel("Units")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig4)

        # To let user download forecast data
        df_forecast = pd.DataFrame({
        'Month': range(1, forecast_months + 1),
        'Forecasted Sales': forecast_sales,
        'Forecasted Profit': forecast_profit
        })
        csv_forecast = df_forecast.to_csv(index=False)

        st.download_button(
        "Download Forecast Data as CSV",
        csv_forecast,
        "forecast_data.csv",
        "text/csv"
        )

    else:
        st.error("⚠️ Price per unit must be greater than variable cost.")


with tab5:
    
    st.header("Sensitivity Analysis")

    if price_per_unit > variable_cost:
        variable_to_test = st.selectbox("Choose variable to test sensitivity:", 
                               ["Price per Unit", "Variable Cost per Unit", "Fixed Costs", "Sales Volume"])

        if variable_to_test == "Price per Unit":
            val_range = st.slider("Price Range ($)", 0.5 * price_per_unit, 1.5 * price_per_unit, (0.8 * price_per_unit, 1.2 * price_per_unit))      # val_range will consist of two numbers (X , Y), val_range[0] would be X which would be min value
            values = np.linspace(val_range[0], val_range[1], 10)                                                                                    # This generates numbers evenly spaced between val_range[0] to val_range[1] with 10 number of points
        elif variable_to_test == "Variable Cost per Unit":
            val_range = st.slider("Variable Cost Range ($)", 0.5 * variable_cost, 1.5 * variable_cost, (0.8 * variable_cost, 1.2 * variable_cost))
            values = np.linspace(val_range[0], val_range[1], 10)
        elif variable_to_test == "Fixed Costs":
            val_range = st.slider("Fixed Costs Range ($)", 0.5 * fixed_costs, 1.5 * fixed_costs, (0.8 * fixed_costs, 1.2 * fixed_costs))
            values = np.linspace(val_range[0], val_range[1], 10)
        else:  
            val_range = st.slider("Sales Volume Range (units)", 0.5 * sales, 1.5 * sales, (0.8 * sales, 1.2 * sales))                               # Sales Volume
            values = np.linspace(val_range[0], val_range[1], 10)

        profits = []                                    # Starts with an empty list to store profits
        for val in values:                              # For each value in the range we are testing, val represents the value we are changing
            if variable_to_test == "Price per Unit":
                cm = val - variable_cost                # Calculating contribution margin based on new price, val represents different prices per unit here
                profit = sales * cm - fixed_costs       # Calculating profit with new price 
            elif variable_to_test == "Variable Cost per Unit":
                cm = price_per_unit - val
                profit = sales * cm - fixed_costs
            elif variable_to_test == "Fixed Costs":
                cm = price_per_unit - variable_cost     # Contribution margin stays the same
                profit = sales * cm - val               # Subtract changed fixed cost to get profit
            else:  
                cm = price_per_unit - variable_cost
                profit = val * cm - fixed_costs

            profits.append(profit)                      # Adds each calculated profit into the profits array

        fig3, ax = plt.subplots()
        ax.plot(values, profits, marker='o')
        ax.set_xlabel(variable_to_test)
        ax.set_ylabel('Profit ($)')
        ax.set_title(f'Sensitivity of Profit to {variable_to_test}')
        ax.grid(True)
        st.pyplot(fig3)

    else:
        st.error("⚠️ Price per unit must be greater than variable cost.")
