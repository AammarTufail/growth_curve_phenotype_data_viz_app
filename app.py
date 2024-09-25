import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from matplotlib.ticker import MultipleLocator

# Function to generate example data with multiple samples
def generate_example_data():
    np.random.seed(42)
    time_points = np.arange(0, 100, 10)
    replicates = 3
    samples = ['Methanosarcina mazei +N', 'Methanosarcina mazei -N']  # Multiple samples
    data_list = []
    for sample in samples:
        mean_values = np.repeat(np.linspace(0.1, 1.2, len(time_points)), replicates)
        data = pd.DataFrame({
            'Time': np.repeat(time_points, replicates),
            'Replicate': np.tile(np.arange(1, replicates + 1), len(time_points)),
            'OD': np.random.normal(loc=mean_values, scale=0.1, size=len(mean_values)),
            'Sample': sample
        })
        data_list.append(data)
    return pd.concat(data_list)

# Function to calculate mean and error (SD or SE)
def calculate_mean_and_error(df, x_column, y_column, error_type='SD'):
    summary = df.groupby([x_column, 'Sample'])[y_column].agg(['mean', 'std', 'count']).reset_index()
    summary.rename(columns={x_column: 'X', 'mean': 'Y'}, inplace=True)
    if error_type == 'SD':
        summary['error'] = summary['std']
    else:
        summary['error'] = summary['std'] / np.sqrt(summary['count'])  # SE
    return summary

# Function to plot using Seaborn/Matplotlib
def plot_seaborn(summary_df, color_palette, x_axis_title, y_axis_title, theme, width, height, show_grid, plot_title, x_limits, y_limits, x_tick_interval, y_tick_interval, legend_position):
    plt.style.use(theme)
    fig, ax = plt.subplots(figsize=(width, height))
    samples = summary_df['Sample'].unique()
    colors = sns.color_palette(color_palette, n_colors=len(samples))
    for idx, sample in enumerate(samples):
        sample_data = summary_df[summary_df['Sample'] == sample]
        ax.errorbar(sample_data['X'], sample_data['Y'], yerr=sample_data['error'], fmt='o', color=colors[idx],
                    ecolor=colors[idx], elinewidth=2, capsize=4, label=sample)
        ax.fill_between(sample_data['X'], sample_data['Y'] - sample_data['error'],
                        sample_data['Y'] + sample_data['error'], color=colors[idx], alpha=0.3)
    ax.set_xlabel(x_axis_title)
    ax.set_ylabel(y_axis_title)
    ax.set_title(plot_title)
    ax.grid(show_grid)
    ax.legend(loc=legend_position)

    # Set x and y limits if provided
    if x_limits[0] is not None and x_limits[1] is not None:
        ax.set_xlim(x_limits)
    if y_limits[0] is not None and y_limits[1] is not None:
        ax.set_ylim(y_limits)

    # Set x and y tick intervals if provided
    if x_tick_interval is not None:
        ax.xaxis.set_major_locator(MultipleLocator(x_tick_interval))
    if y_tick_interval is not None:
        ax.yaxis.set_major_locator(MultipleLocator(y_tick_interval))

    st.pyplot(fig)
    return fig

# Streamlit Layout
st.set_page_config(layout="wide", page_title="Growth Curve Visualization")

st.title("Growth Curve Visualization of Methanosarcina mazei")

st.write("""
Welcome to the growth curve visualization tool. Use this app to visualize the growth of Methanosarcina mazei over time. You can upload your own data, select different error types, customize the plot colors, and adjust the plot appearance.
""")

# Sidebar - Download Template Dataset
st.sidebar.header("Download Template Dataset")

# Generate example data
df_template = generate_example_data()

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    processed_data = output.getvalue()
    return processed_data

data_xlsx = to_excel(df_template)
st.sidebar.download_button(label='Download Template as Excel', data=data_xlsx, file_name='template_dataset.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Allow the user to upload their own data
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Sidebar for general plot settings
st.sidebar.header("Plot Settings")

# Plot title input
plot_title = st.sidebar.text_input("Plot Title", "Growth Curve of Methanosarcina mazei")

# Error type selector
error_type = st.sidebar.radio("Select Error Type", options=["Standard Deviation (SD)", "Standard Error (SE)"])

# Color palette selection
color_palettes = ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind']
selected_palette = st.sidebar.selectbox("Select Color Palette", options=color_palettes)

# Plot size selection
width = st.sidebar.slider("Select Plot Width", min_value=5, max_value=20, value=8)
height = st.sidebar.slider("Select Plot Height", min_value=3, max_value=12, value=4)

# Select theme style
static_themes = plt.style.available
theme = st.sidebar.selectbox("Select Plot Theme", options=static_themes, index=static_themes.index('classic'))

# Grid lines option
show_grid = st.sidebar.checkbox("Show Grid Lines", value=False)

# Data processing
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            data_to_plot = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data_to_plot = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.stop()
else:
    data_to_plot = df_template

# Check if 'Sample' column exists, if not, add a default sample
if 'Sample' not in data_to_plot.columns:
    data_to_plot['Sample'] = 'Sample 1'

# Set x_column and y_column directly
x_column = 'Time'
y_column = 'OD'

# Arrange items before the plot in two columns
col1, col2 = st.columns(2)

with col1:
    # Axis title inputs based on column headers
    x_axis_title = st.text_input("X-axis Title", x_column)
    y_axis_title = st.text_input("Y-axis Title", y_column)

    # Option to display data before plotting
    show_data = st.checkbox("Display data before plotting?")
    if show_data:
        st.write("Data Preview:")
        st.dataframe(data_to_plot)

    # Axis Limits
    st.subheader("Axis Limits")

    use_x_limits = st.checkbox("Set X-axis limits?", value=False)
    if use_x_limits:
        x_min_default = data_to_plot[x_column].min()
        x_max_default = data_to_plot[x_column].max()
        x_min = st.number_input("X-axis minimum", value=float(x_min_default), step=0.1, format="%.2f")
        x_max = st.number_input("X-axis maximum", value=float(x_max_default), step=0.1, format="%.2f")
        x_limits = (x_min, x_max)
    else:
        x_limits = (None, None)

    use_y_limits = st.checkbox("Set Y-axis limits?", value=False)
    if use_y_limits:
        y_min_default = data_to_plot[y_column].min()
        y_max_default = data_to_plot[y_column].max()
        y_min = st.number_input("Y-axis minimum", value=float(y_min_default), step=0.1, format="%.2f")
        y_max = st.number_input("Y-axis maximum", value=float(y_max_default), step=0.1, format="%.2f")
        y_limits = (y_min, y_max)
    else:
        y_limits = (None, None)

with col2:
    # Legend Position
    legend_positions = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',
                        'center left', 'center right', 'lower center', 'upper center', 'center']
    legend_position = st.selectbox("Select Legend Position", options=legend_positions, index=0)

    # Tick Intervals
    st.subheader("Tick Intervals")

    use_x_tick_interval = st.checkbox("Set X-axis tick interval?", value=False)
    if use_x_tick_interval:
        x_tick_interval = st.number_input("X-axis tick interval", value=10.0, min_value=0.0, max_value=10000.0, step=0.1, format="%.2f")
    else:
        x_tick_interval = None

    use_y_tick_interval = st.checkbox("Set Y-axis tick interval?", value=False)
    if use_y_tick_interval:
        y_tick_interval = st.number_input("Y-axis tick interval", value=0.2, min_value=0.0, max_value=10000.0, step=0.1, format="%.2f")
    else:
        y_tick_interval = None

# Calculate summary statistics
summary_df = calculate_mean_and_error(data_to_plot, x_column, y_column, error_type='SD' if error_type == "Standard Deviation (SD)" else 'SE')

# Plotting
st.header("Growth Curve Plot")
fig = plot_seaborn(summary_df, selected_palette, x_axis_title, y_axis_title, theme, width, height, show_grid,
                   plot_title, x_limits, y_limits, x_tick_interval, y_tick_interval, legend_position)

# Save Plot Options
st.header("Save the Plot")

save_width = st.number_input("Width (inches) for saved plot", value=float(width), min_value=1.0, max_value=100.0, step=1.0)
save_height = st.number_input("Height (inches) for saved plot", value=float(height), min_value=1.0, max_value=100.0, step=1.0)
save_dpi = st.number_input("Resolution (DPI) for saved plot", value=300, min_value=50, max_value=1200, step=50)
file_format = st.selectbox("Select File Format", options=["PNG", "SVG", "PDF"])

# Adjust figure size for saving
fig.set_size_inches(save_width, save_height)

buf = BytesIO()
fig.savefig(buf, format=file_format.lower(), dpi=save_dpi, bbox_inches='tight')
st.download_button(
    label=f"Download plot as {file_format}",
    data=buf.getvalue(),
    file_name=f'growth_curve.{file_format.lower()}',
    mime=f'image/{file_format.lower()}'
)
