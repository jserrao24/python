import pandas as pd
import plotly.graph_objects as go
import webbrowser

print("Script started")

# Load the CSV file
#remove honolulu string from column

Neighborhood_Zhvi_AllHomes = pd.read_csv('Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', index_col=[3,2,4,5])
print("CSV loaded successfully")

Neighborhood_Zhvi_AllHomes.index = Neighborhood_Zhvi_AllHomes.index.set_levels(Neighborhood_Zhvi_AllHomes.index.levels[0].str.replace('honolulu', ''), level=0)

# Extract columns containing dates
date_columns = Neighborhood_Zhvi_AllHomes.columns[Neighborhood_Zhvi_AllHomes.columns.str.match(r'\d{1,2}/\d{1,2}/\d{4}')]

# Convert the date columns to a datetime index
#cretae data variable adddate columns
#index the data of the date columns 
data = Neighborhood_Zhvi_AllHomes[date_columns].T
data.index = pd.to_datetime(data.index)


#create neighborhood city varialbe
# Handle non-numeric values by coercing them to numeric, NaN will be inserted for non-numeric values
# Calculate the sum of rows and count of rows
#print to console sum of rows and count of rows
Neighborhood_Zhvi_AllHomes_numeric = Neighborhood_Zhvi_AllHomes.apply(pd.to_numeric, errors='coerce')
sum_rows = Neighborhood_Zhvi_AllHomes_numeric.sum().sum()
count_rows = len(Neighborhood_Zhvi_AllHomes_numeric)

print("Sum of rows:", sum_rows)
print("Count of rows:", count_rows)

# Filter out non-numeric values before sorting, drop them if not a number
# set new top 5 variable equal to teh now should be numeric values, use head to get the top 5
#print the top 5 rows with the highest USD values in 2024 variable and the string saying it


Neighborhood_Zhvi_AllHomes_numeric_2024 = Neighborhood_Zhvi_AllHomes_numeric['4/30/2024'].dropna()
top_5_rows_2024 = Neighborhood_Zhvi_AllHomes_numeric_2024.sort_values(ascending=False).head(5)
print("Top 5 rows with the highest USD values in 2024:")
print(top_5_rows_2024)

# Set  tracesarray,Create traces for each location to track 
#iterate through every column with the location, remember location can be anything could be i, we just name it that
# plot on pllotly using the trace array
#while iterating for every data column apend them to the traces array
traces = []

for location in data.columns:
    trace = go.Scatter(x=data.index, y=data[location], mode='lines', name=str(location), showlegend=True)
    traces.append(trace)

# Count the number of plot points being shown
num_plot_points = len(traces)

# Create the layout
#set teh title 
#set teh x asiss with title
#set y axis
layout = go.Layout(
    title='Monthly Values Over Time',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Value (USD)')
)

# Add annotation for the number of plot points
annotation = go.layout.Annotation(
    text=f"Number of plot points: {num_plot_points}",
    xref="paper",
    yref="paper",
    x=0.95,
    y=0.05,
    showarrow=False
)
layout['annotations'] = [annotation]

# Create the figure varialble
fig = go.Figure(data=traces, layout=layout)

# Define JavaScript code to handle click events
#include sctp tag
#add the on click to make reposnive
javascript = """
<script>
    document.getElementById('graph').on('plotly_click', function(data) {
        var selected_index = data.points[0].pointNumber;
        var traces = document.getElementById('graph').data;
        for (var i = 0; i < traces.length; i++) {
            if (i == selected_index) {
                Plotly.restyle('graph', {visible: true}, [i]);
            } else {
                Plotly.restyle('graph', {visible: false}, [i]);
            }
        }
    });
</script>
"""

# Generate HTML file
with open("index.html", "w") as file:
    file.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    file.write(javascript)

# Open the HTML file in a web browser
webbrowser.open_new_tab("index.html")

print("Script completed")
