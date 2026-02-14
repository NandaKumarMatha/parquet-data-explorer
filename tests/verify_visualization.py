import sys
import os
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QApplication
from ui.visualization_widget import VisualizationWidget

def test_visualization_widget():
    app = QApplication(sys.argv)
    
    # Create sample data
    df = pd.DataFrame({
        'A': np.random.rand(100),
        'B': np.random.rand(100) * 100,
        'C': np.random.choice(['X', 'Y', 'Z'], 100),
        'D': np.random.randint(0, 50, 100)
    })
    
    widget = VisualizationWidget()
    widget.set_dataframe(df)
    
    # Test plotting Histogram
    widget.chart_type_combo.setCurrentText("Histogram")
    widget.x_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Histogram plotted successfully")
    
    # Test plotting Scatter
    widget.chart_type_combo.setCurrentText("Scatter Plot")
    widget.x_col_combo.setCurrentText("A")
    widget.y_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Scatter Plot plotted successfully")

    # Test plotting Bar Chart
    widget.chart_type_combo.setCurrentText("Bar Chart")
    widget.x_col_combo.setCurrentText("C")
    widget.y_col_combo.setCurrentText("D")
    widget.plot_chart()
    print("Bar Chart plotted successfully")
    
    # Test plotting Line Chart
    widget.chart_type_combo.setCurrentText("Line Chart")
    widget.x_col_combo.setCurrentText("A")
    widget.y_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Line Chart plotted successfully")

    # Test plotting Box Plot
    widget.chart_type_combo.setCurrentText("Box Plot")
    widget.x_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Box Plot plotted successfully")

    # Test plotting Pie Chart
    widget.chart_type_combo.setCurrentText("Pie Chart")
    widget.x_col_combo.setCurrentText("C")
    widget.plot_chart()
    print("Pie Chart plotted successfully")

    # Test plotting Area Chart
    widget.chart_type_combo.setCurrentText("Area Chart")
    widget.x_col_combo.setCurrentText("A") # A is sorted in plot logic or should be? Logic says sorts by X.
    widget.y_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Area Chart plotted successfully")

    # Test plotting Hexbin Plot
    widget.chart_type_combo.setCurrentText("Hexbin Plot")
    widget.x_col_combo.setCurrentText("A")
    widget.y_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Hexbin Plot plotted successfully")

    # Test plotting Violin Plot
    widget.chart_type_combo.setCurrentText("Violin Plot")
    widget.x_col_combo.setCurrentText("C")
    widget.y_col_combo.setCurrentText("B")
    widget.plot_chart()
    print("Violin Plot plotted successfully")

    # Test plotting Correlation Heatmap
    widget.chart_type_combo.setCurrentText("Correlation Heatmap")
    widget.plot_chart()
    print("Correlation Heatmap plotted successfully")

    # Test plotting Geo Scatter Plot
    # Create mock lat/lon data if not distinct enough, but scatter works generally
    widget.chart_type_combo.setCurrentText("Geo Scatter Plot")
    widget.x_col_combo.setCurrentText("A") # Treat A as Longitude
    widget.y_col_combo.setCurrentText("B") # Treat B as Latitude
    widget.plot_chart()
    print("Geo Scatter Plot plotted successfully")

    # Test plotting Choropleth Map
    # Need a dataframe with country names
    df_countries = pd.DataFrame({
        'Country': ['United States of America', 'India', 'China', 'Brazil', 'France', 'Russia'],
        'Value': [100, 90, 80, 70, 60, 50]
    })
    widget.set_dataframe(df_countries)
    widget.chart_type_combo.setCurrentText("Choropleth Map")
    widget.x_col_combo.setCurrentText("Country")
    widget.y_col_combo.setCurrentText("Value")
    widget.plot_chart()
    print("Choropleth Map plotted successfully")
    
    print("All tests passed!")
    # Allow the app to exit
    # sys.exit(0) 

if __name__ == "__main__":
    try:
        test_visualization_widget()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
