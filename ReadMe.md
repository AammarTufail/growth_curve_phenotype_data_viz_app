# Growth Curve Visualization Application

Welcome to the **Growth Curve Visualization Application**! This interactive Streamlit app allows you to visualize the growth of any microorganism over time using your own data. Customize plots extensively and export high-quality figures for your presentations or publications.

Developed by [**Muhammad Aammar Tufail (PhD)**](https://github.com/AammarTufail)

## Table of Contents

- [Growth Curve Visualization Application](#growth-curve-visualization-application)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Usage Instructions](#usage-instructions)
  - [Dependencies](#dependencies)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)

---

## Features

- **Data Upload**: Import your dataset in CSV or Excel format.
- **Template Dataset**: Download a sample dataset to understand the required data format.
- **Interactive Customization**: Adjust plot settings, fonts, colors, and more in real-time.
- **Statistical Options**: Choose between mean or median calculations and select error types (Standard Deviation or Standard Error).
- **Visualization Options**:
  - Customize axis titles, limits, and scales.
  - Select different themes and color palettes.
  - Adjust line styles, markers, and scatter point sizes.
- **Export Options**: Save your customized plots in PNG, SVG, or PDF formats with adjustable dimensions and resolution.

## Installation

### Prerequisites

- **Python**: Version 3.7 or higher
- **pip**: Python package installer

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AammarTufail/growth_curve_phenotype_data_viz_app
   cd growth_curve_phenotype_data_viz_app
   ```


2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**

   Install the required packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, you can install packages individually:*

   ```bash
   pip install streamlit pandas numpy matplotlib seaborn openpyxl xlsxwriter
   ```

## Usage Instructions

1. **Run the Application**

   ```bash
   streamlit run app.py
   ```

   - The app will open in your default web browser.
   - If it doesn't open automatically, navigate to the URL provided in the terminal (usually `http://localhost:8501`).

2. **Uploading Data**

   - Use the sidebar to upload your dataset in CSV or Excel format.
   - If you don't have your own data, you can download the template dataset provided in the sidebar.

3. **Data Format**

   Your dataset should contain the following columns:

   - **Time**: The time points of your measurements.
   - **OD**: The observed data (e.g., optical density).
   - **Replicate**: Replicate number (if applicable).
   - **Sample**: Sample or condition name.

   **Note:** If the 'Sample' column is missing, a default sample name 'Sample 1' will be assigned.

4. **Customizing the Plot**

   - **Data Settings**: Choose calculation type (Mean or Median) and error type (Standard Deviation or Standard Error). Select the Y-axis scale (Linear, Log, Log10).
   - **Axis Settings**: Adjust axis titles, limits, tick intervals, and decide whether to show grid lines or remove borders.
   - **Font Settings**: Customize font family, size, style, and weight for axis labels, titles, and tick labels.
   - **Legend Settings**: Set legend position and customize font properties.
   - **Line and Color Settings**:
     - Choose to use different colors, markers, or line styles for each sample.
     - Select color palettes or use custom colors.
     - Adjust line width, opacity, error bar properties, and scatter point size.
   - **Plot Settings**: Set the plot title and adjust the plot's width and height.

   *All these options are available in the sidebar under respective sections.*

5. **Viewing the Plot**

   - The plot updates automatically as you adjust settings.
   - Use the "Display data before plotting?" checkbox to preview your dataset within the app.

6. **Saving the Plot**

   - Scroll to the "Save the Plot" section below the plot.
   - Adjust the width, height, and resolution (DPI) for the saved plot.
   - Choose the file format (PNG, SVG, PDF).
   - Click the "Download plot as [format]" button to save your customized plot.

## Dependencies

- **Python Packages**:
  - streamlit
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - openpyxl
  - xlsxwriter

- **`requirements.txt` File**:

  ```plaintext
    streamlit==1.36.0
    pandas==2.2.0
    numpy==1.26.4
    matplotlib==3.8.3
    seaborn==0.13.2
    openpyxl==3.1.2
    xlsxwriter==3.2.0
  ```

  *You can install all dependencies using:*

  ```bash
  pip install -r requirements.txt
  ```

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **Developer**: [Muhammad Aammar Tufail (PhD)](https://github.com/AammarTufail)
- **Contributors**: Thanks to all contributors of the open-source libraries utilized in this project.

## Contact

For questions, suggestions, or contributions, please contact:

- **Email**: [your.email@example.com](mailto:m.aammar.tufail@gmail.com)
- **GitHub**: [https://github.com/AammarTufail/growth_curve_phenotype_data_viz_app](https://github.com/AammarTufail/growth_curve_phenotype_data_viz_app)

*Feel free to open an issue or pull request if you encounter any problems or have ideas for enhancements.*

---

*This README was generated to provide clear instructions and facilitate the use of the Growth Curve Visualization Application.*