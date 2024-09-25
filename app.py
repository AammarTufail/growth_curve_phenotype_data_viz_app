import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from matplotlib.ticker import MultipleLocator
import matplotlib.colors as mc

# Function to adjust color brightness
def adjust_color_brightness(color, amount=0.7):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = mc.to_rgb(c)
    c = [max(0, min(1, amount * x)) for x in c]
    return c

# Cache the data generation function
@st.cache_data
def generate_example_data():
    np.random.seed(42)
    time_points = np.arange(0, 100, 10)
    replicates = 3
    samples = ['Methanosarcina mazei +N', 'Methanosarcina mazei -N', 'Methanosarcina mazei +S']
    data_list = []
    for sample in samples:
        if sample == 'Methanosarcina mazei +N':
            mean_values = np.repeat(np.linspace(0.1, 1.2, len(time_points)), replicates)
        elif sample == 'Methanosarcina mazei -N':
            mean_values = np.repeat(np.linspace(0.2, 1.0, len(time_points)), replicates)
        elif sample == 'Methanosarcina mazei +S':
            mean_values = np.repeat(np.linspace(0.3, 1.5, len(time_points)), replicates)
        else:
            mean_values = np.repeat(np.linspace(0.1, 1.2, len(time_points)), replicates)
        data = pd.DataFrame({
            'Time': np.repeat(time_points, replicates),
            'Replicate': np.tile(np.arange(1, replicates + 1), len(time_points)),
            'OD': np.random.normal(loc=mean_values, scale=0.1, size=len(mean_values)),
            'Sample': sample
        })
        data_list.append(data)
    return pd.concat(data_list)

# Cache the calculation function
@st.cache_data
def calculate_mean_and_error(df, x_column, y_column, error_type='SD', calculation_type='Mean'):
    if calculation_type == 'Mean':
        summary = df.groupby([x_column, 'Sample'])[y_column].agg(['mean', 'std', 'count']).reset_index()
        summary.rename(columns={x_column: 'X', 'mean': 'Y'}, inplace=True)
    else:
        summary = df.groupby([x_column, 'Sample'])[y_column].agg(['median', 'std', 'count']).reset_index()
        summary.rename(columns={x_column: 'X', 'median': 'Y'}, inplace=True)
    if error_type == 'SD':
        summary['error'] = summary['std']
    else:
        summary['error'] = summary['std'] / np.sqrt(summary['count'])
    return summary

def plot_seaborn(summary_df, x_axis_title, y_axis_title, plot_title, theme, width, height, show_grid,
                 x_limits, y_limits, x_tick_interval, y_tick_interval, legend_position,
                 y_scale, remove_borders, use_different_colors, use_custom_colors, use_different_markers,
                 use_different_line_styles, custom_colors,
                 font_family, axis_label_font_size, axis_label_font_style, axis_label_font_weight,
                 title_font_size, title_font_style, title_font_weight, tick_label_font_size,
                 tick_label_font_style, tick_label_font_weight,
                 legend_font_size, legend_font_family, legend_font_style, legend_font_weight,
                 line_width, opacity, errorbar_line_width, errorbar_capsize, scatter_point_size,
                 selected_palette='Set2'):
    plt.style.use(theme)
    fig, ax = plt.subplots(figsize=(width, height))
    samples = summary_df['Sample'].unique()
    markers_list = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']
    line_styles_list = ['-', '--', '-.', ':']
    if use_different_markers:
        markers = [markers_list[i % len(markers_list)] for i in range(len(samples))]
    else:
        markers = ['o'] * len(samples)
    if use_different_line_styles:
        line_styles = [line_styles_list[i % len(line_styles_list)] for i in range(len(samples))]
    else:
        line_styles = ['-'] * len(samples)
    if use_different_colors:
        if use_custom_colors and custom_colors:
            colors = []
            for idx, sample in enumerate(samples):
                if custom_colors.get(sample):
                    colors.append(custom_colors[sample])
                else:
                    colors.append(sns.color_palette(selected_palette, n_colors=len(samples))[idx])
        else:
            colors = sns.color_palette(selected_palette, n_colors=len(samples))
    else:
        default_color = sns.color_palette(selected_palette, n_colors=1)[0]
        colors = [default_color] * len(samples)
    for idx, sample in enumerate(samples):
        sample_data = summary_df[summary_df['Sample'] == sample]
        marker = markers[idx]
        line_style = line_styles[idx]
        color = colors[idx]
        darker_color = adjust_color_brightness(color, amount=0.7)
        ax.plot(sample_data['X'], sample_data['Y'], linestyle=line_style, marker=marker,
                color=darker_color, label=sample, linewidth=line_width, alpha=opacity,
                markersize=scatter_point_size)
        ax.errorbar(sample_data['X'], sample_data['Y'], yerr=sample_data['error'], fmt='None',
                    ecolor=color, elinewidth=errorbar_line_width, capsize=errorbar_capsize, alpha=opacity)
        ax.fill_between(sample_data['X'], sample_data['Y'] - sample_data['error'],
                        sample_data['Y'] + sample_data['error'], color=color, alpha=opacity*0.3)
    ax.set_xlabel(x_axis_title, fontsize=axis_label_font_size, fontfamily=font_family,
                  fontstyle=axis_label_font_style, fontweight=axis_label_font_weight)
    ax.set_ylabel(y_axis_title, fontsize=axis_label_font_size, fontfamily=font_family,
                  fontstyle=axis_label_font_style, fontweight=axis_label_font_weight)
    ax.set_title(plot_title, fontsize=title_font_size, fontfamily=font_family,
                 fontstyle=title_font_style, fontweight=title_font_weight)
    for tick in ax.get_xticklabels():
        tick.set_fontsize(tick_label_font_size)
        tick.set_fontfamily(font_family)
        tick.set_fontstyle(tick_label_font_style)
        tick.set_fontweight(tick_label_font_weight)
    for tick in ax.get_yticklabels():
        tick.set_fontsize(tick_label_font_size)
        tick.set_fontfamily(font_family)
        tick.set_fontstyle(tick_label_font_style)
        tick.set_fontweight(tick_label_font_weight)
    ax.grid(show_grid)
    ax.legend(loc=legend_position, prop={'size': legend_font_size, 'family': legend_font_family,
                                         'style': legend_font_style, 'weight': legend_font_weight})
    if x_limits[0] is not None and x_limits[1] is not None:
        ax.set_xlim(x_limits)
    if y_limits[0] is not None and y_limits[1] is not None:
        ax.set_ylim(y_limits)
    if x_tick_interval is not None:
        ax.xaxis.set_major_locator(MultipleLocator(x_tick_interval))
    if y_tick_interval is not None:
        ax.yaxis.set_major_locator(MultipleLocator(y_tick_interval))
    if y_scale == "Linear":
        pass
    elif y_scale == "Log":
        ax.set_yscale('log')
    elif y_scale == "Log10":
        ax.set_yscale('log', base=10)
    if remove_borders:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='both', which='both', top=False, right=False)
    return fig

# Streamlit Layout
st.set_page_config(layout="wide", page_title="Growth Curve Visualization")

st.title("Growth Curve Visualization Application")
# subtitle
st.subheader("Visualize the growth of any microorganism over time Developed by [Muhammad Aammar Tufail (PhD)](https://github.com/AammarTufail)")

st.write("""
Welcome to the growth curve visualization tool. Use this app to visualize the growth of any microorganism over time. You can upload your own data, select different error types, customize the plot colors, and adjust the plot appearance.
""")
# Add major Heading of Sidebar with Emojis
st.sidebar.title("Use your Data or Download Template Dataset 📊")

# Sidebar - Download Template Dataset
st.sidebar.header("Download Template Dataset")
st.sidebar.write("""                 
                 **Note:** You can download the template dataset to see the required format for the data, and then upload your own data within same format
                """)
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

# Option to display data before plotting
show_data = st.checkbox("Display data before plotting?")
if show_data:
    st.write("Data Preview:")
    st.dataframe(data_to_plot)

# Settings in Sidebar
st.sidebar.title("📊 Plot Settings")
# Data Settings
with st.sidebar.expander("Data Settings", expanded=False):
    calculation_type = st.radio("Select Calculation Type", options=["Mean", "Median"], index=0)
    error_type = st.radio("Select Error Type", options=["Standard Deviation (SD)", "Standard Error (SE)"], index=1)
    y_scale = st.selectbox("Select Y-axis Scale", options=["Linear", "Log", "Log10"], index=0)

# Axis Settings
with st.sidebar.expander("Axis Settings", expanded=False):
    x_axis_title = st.text_input("X-axis Title", x_column)
    use_x_limits = st.checkbox("Set X-axis limits?", value=False)
    if use_x_limits:
        x_min_default = data_to_plot[x_column].min()
        x_max_default = data_to_plot[x_column].max()
        x_min = st.number_input("X-axis minimum", value=float(x_min_default), step=0.1, format="%.2f")
        x_max = st.number_input("X-axis maximum", value=float(x_max_default), step=0.1, format="%.2f")
        x_limits = (x_min, x_max)
    else:
        x_limits = (None, None)

    use_x_tick_interval = st.checkbox("Set X-axis tick interval?", value=False)
    if use_x_tick_interval:
        x_tick_interval = st.number_input("X-axis tick interval", value=10.0, min_value=0.0, max_value=10000.0,
                                          step=0.1, format="%.2f")
    else:
        x_tick_interval = None

    y_axis_title = st.text_input("Y-axis Title", y_column)
    use_y_limits = st.checkbox("Set Y-axis limits?", value=False)
    if use_y_limits:
        y_min_default = data_to_plot[y_column].min()
        y_max_default = data_to_plot[y_column].max()
        y_min = st.number_input("Y-axis minimum", value=float(y_min_default), step=0.1, format="%.2f")
        y_max = st.number_input("Y-axis maximum", value=float(y_max_default), step=0.1, format="%.2f")
        y_limits = (y_min, y_max)
    else:
        y_limits = (None, None)

    use_y_tick_interval = st.checkbox("Set Y-axis tick interval?", value=False)
    if use_y_tick_interval:
        y_tick_interval = st.number_input("Y-axis tick interval", value=0.2, min_value=0.0, max_value=10000.0,
                                          step=0.1, format="%.2f")
    else:
        y_tick_interval = None

    show_grid = st.checkbox("Show Grid Lines", value=False)
    remove_borders = st.checkbox("Remove top and right borders?", value=True)

    static_themes = plt.style.available
    theme = st.selectbox("Select Plot Theme", options=static_themes, index=static_themes.index('classic'))

# Font Settings
with st.sidebar.expander("Font Settings", expanded=False):
    font_families = ['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy']
    font_family = st.selectbox("Select Font Family", options=font_families, index=0)

    axis_label_font_size = st.number_input("Axis Label Font Size", value=12, min_value=1, max_value=100)
    axis_label_font_style = st.selectbox("Axis Label Font Style", options=['normal', 'italic', 'oblique'], index=0)
    axis_label_font_weight = st.selectbox("Axis Label Font Weight", options=['normal', 'bold'], index=0)

    title_font_size = st.number_input("Title Font Size", value=14, min_value=1, max_value=100)
    title_font_style = st.selectbox("Title Font Style", options=['normal', 'italic', 'oblique'], index=0)
    title_font_weight = st.selectbox("Title Font Weight", options=['normal', 'bold'], index=0)

    tick_label_font_size = st.number_input("Tick Label Font Size", value=10, min_value=1, max_value=100)
    tick_label_font_style = st.selectbox("Tick Label Font Style", options=['normal', 'italic', 'oblique'], index=0)
    tick_label_font_weight = st.selectbox("Tick Label Font Weight", options=['normal', 'bold'], index=0)

# Legend Settings
with st.sidebar.expander("Legend Settings", expanded=False):
    legend_positions = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',
                        'center left', 'center right', 'lower center', 'upper center', 'center']
    legend_position = st.selectbox("Select Legend Position", options=legend_positions, index=0)
    legend_font_size = st.number_input("Legend Font Size", value=10, min_value=1, max_value=100)
    legend_font_family = st.selectbox("Legend Font Family", options=font_families, index=0)
    legend_font_style = st.selectbox("Legend Font Style", options=['normal', 'italic', 'oblique'], index=0)
    legend_font_weight = st.selectbox("Legend Font Weight", options=['normal', 'bold'], index=0)

# Line and Color Settings
with st.sidebar.expander("Line and Color Settings", expanded=False):
    use_different_colors = st.checkbox("Use different colors for samples?", value=True)
    color_palettes = ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind', 'Set1', 'Set2', 'Set3', 'tab10']
    selected_palette = st.selectbox("Select Color Palette", options=color_palettes, index=color_palettes.index('Set2'))
    use_custom_colors = False
    custom_colors = {}
    if use_different_colors:
        use_custom_colors = st.checkbox("Use custom colors?", value=False)
        if use_custom_colors:
            samples = data_to_plot['Sample'].unique()
            for sample in samples:
                color = st.color_picker(f"Select color for {sample}")
                custom_colors[sample] = color
    else:
        default_color = sns.color_palette(selected_palette, n_colors=1)[0]
        custom_colors['default'] = default_color

    use_different_markers = st.checkbox("Use different markers for samples?", value=False)
    use_different_line_styles = st.checkbox("Use different line styles for samples?", value=False)
    line_width = st.number_input("Line Width", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
    opacity = st.slider("Color Opacity", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

    # Error bar settings
    errorbar_line_width = st.number_input("Error Bar Line Width", value=0.5, min_value=0.1, max_value=10.0, step=0.1)
    errorbar_capsize = st.number_input("Error Bar Capsize", value=2.0, min_value=0.0, max_value=20.0, step=0.5)

    # Add the size of scatter points
    scatter_point_size = st.number_input("Scatter Point Size", value=5, min_value=1, max_value=20)

# Plot Settings
with st.sidebar.expander("Plot Settings", expanded=False):
    plot_title = st.text_input("Plot Title", "Growth Curve")
    width = st.slider("Plot Width (inches)", value=8.0, min_value=1.0, max_value=20.0, step=0.5)
    height = st.slider("Plot Height (inches)", value=3.0, min_value=1.0, max_value=20.0, step=0.5)

# Process data and calculate mean and error
error_type_mapping = {'Standard Deviation (SD)': 'SD', 'Standard Error (SE)': 'SE'}
error_type_selected = error_type_mapping[error_type]

summary_df = calculate_mean_and_error(data_to_plot, x_column, y_column, error_type=error_type_selected, calculation_type=calculation_type)

# Call the plotting function
fig = plot_seaborn(summary_df, x_axis_title, y_axis_title, plot_title, theme, width, height, show_grid,
                   x_limits, y_limits, x_tick_interval, y_tick_interval, legend_position,
                   y_scale, remove_borders, use_different_colors, use_custom_colors, use_different_markers,
                   use_different_line_styles, custom_colors,
                   font_family, axis_label_font_size, axis_label_font_style, axis_label_font_weight,
                   title_font_size, title_font_style, title_font_weight, tick_label_font_size,
                   tick_label_font_style, tick_label_font_weight,
                   legend_font_size, legend_font_family, legend_font_style, legend_font_weight,
                   line_width, opacity, errorbar_line_width, errorbar_capsize, scatter_point_size,
                   selected_palette=selected_palette)

st.pyplot(fig)
# Save Plot Options
st.header("Save the Plot")

col1, col2, col3 = st.columns(3)
with col1:
    save_width = st.number_input("Width (inches) for saved plot", value=8.0, min_value=1.0, max_value=100.0, step=1.0)
with col2:
    save_height = st.number_input("Height (inches) for saved plot", value=6.0, min_value=1.0, max_value=100.0, step=1.0)
with col3:
    save_dpi = st.number_input("Resolution (DPI) for saved plot", value=300, min_value=50, max_value=1200, step=50)
file_format = st.selectbox("Select File Format", options=["PNG", "SVG", "PDF"])
fig.set_size_inches(save_width, save_height)

buf = BytesIO()
fig.savefig(buf, format=file_format.lower(), dpi=save_dpi, bbox_inches='tight')
st.download_button(
    label=f"Download plot as {file_format}",
    data=buf.getvalue(),
    file_name=f'growth_curve.{file_format.lower()}',
    mime=f'image/{file_format.lower()}'
)