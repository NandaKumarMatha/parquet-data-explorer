from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg') # Use Qt backend, works for Qt6 too usually, or try 'QtAgg' if available in newer versions
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
import json
import os

class VisualizationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Controls
        controls_layout = QHBoxLayout()
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Histogram", "Scatter Plot", "Bar Chart", "Line Chart", "Box Plot", 
                                        "Pie Chart", "Area Chart", "Hexbin Plot", "Violin Plot", "Correlation Heatmap",
                                        "Geo Scatter Plot", "Choropleth Map"])
        self.chart_type_combo.currentTextChanged.connect(self.update_column_selectors)
        controls_layout.addWidget(QLabel("Chart Type:"))
        controls_layout.addWidget(self.chart_type_combo)

        self.x_col_combo = QComboBox()
        controls_layout.addWidget(QLabel("X Column:"))
        controls_layout.addWidget(self.x_col_combo)

        self.y_col_combo = QComboBox()
        self.y_label = QLabel("Y Column:")
        controls_layout.addWidget(self.y_label)
        controls_layout.addWidget(self.y_col_combo)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_chart)
        controls_layout.addWidget(self.plot_button)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Chart area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        
        # Initial state
        self.update_column_selectors()

    def set_dataframe(self, df):
        self.df = df
        self.update_column_combo_boxes()

    def update_column_combo_boxes(self):
        self.x_col_combo.clear()
        self.y_col_combo.clear()
        if not self.df.empty:
            columns = self.df.columns.tolist()
            self.x_col_combo.addItems(columns)
            self.y_col_combo.addItems(columns)

    def update_column_selectors(self):
        chart_type = self.chart_type_combo.currentText()
        if chart_type in ["Histogram", "Box Plot", "Pie Chart"]:
            self.y_col_combo.setVisible(False)
            self.y_label.setVisible(False)
            self.x_col_combo.setVisible(True) # Ensure X is visible
            self.x_col_combo.parentWidget().findChildren(QLabel)[1].setVisible(True)
        elif chart_type == "Correlation Heatmap":
            self.x_col_combo.setVisible(False)
            self.y_col_combo.setVisible(False)
            self.y_label.setVisible(False)
            # Hack to hide labels if we could, but skipping for now
        elif chart_type == "Choropleth Map":
            # X = Country Name / ISO Code, Y = Value (Color)
            self.y_col_combo.setVisible(True)
            self.y_label.setVisible(True)
            self.x_col_combo.setVisible(True)
            self.y_label.setText("Value Column:") # Rename logic if possible, or just user knows
        else:
            self.y_col_combo.setVisible(True)
            self.y_label.setVisible(True)
            self.x_col_combo.setVisible(True)
            self.y_label.setText("Y Column:") if hasattr(self, 'y_label') else None

    def plot_chart(self):
        if self.df.empty:
            QMessageBox.warning(self, "No Data", "No data to plot.")
            return

        chart_type = self.chart_type_combo.currentText()
        x_col = self.x_col_combo.currentText()
        y_col = self.y_col_combo.currentText()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        try:
            if chart_type == "Histogram":
                if not pd.api.types.is_numeric_dtype(self.df[x_col]):
                     raise ValueError(f"Column '{x_col}' must be numeric for Histogram.")
                ax.hist(self.df[x_col].dropna(), bins=20)
                ax.set_title(f"Histogram of {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel("Frequency")

            elif chart_type == "Scatter Plot":
                if not pd.api.types.is_numeric_dtype(self.df[x_col]) or not pd.api.types.is_numeric_dtype(self.df[y_col]):
                    raise ValueError("Both columns must be numeric for Scatter Plot.")
                ax.scatter(self.df[x_col], self.df[y_col], alpha=0.5)
                ax.set_title(f"{x_col} vs {y_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
            
            elif chart_type == "Bar Chart":
                # Aggregate for bar chart if there are many unique values, or just plot head
                # For simplicity, let's plot raw values but warn if too many
                if len(self.df) > 100:
                     QMessageBox.information(self, "Warning", "Plotting specific rows. For aggregated bar charts, implement grouping.")
                     plot_df = self.df.head(50)
                else:
                    plot_df = self.df
                
                ax.bar(plot_df[x_col].astype(str), plot_df[y_col])
                ax.set_title(f"{y_col} by {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                # Rotate x labels if they are strings
                if pd.api.types.is_object_dtype(plot_df[x_col]) or pd.api.types.is_categorical_dtype(plot_df[x_col]):
                     ax.tick_params(axis='x', rotation=45)

            elif chart_type == "Line Chart":
                # Sort by X usually makes sense for line charts
                plot_df = self.df.sort_values(by=x_col)
                ax.plot(plot_df[x_col], plot_df[y_col])
                ax.set_title(f"{y_col} over {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

                ax.boxplot(self.df[x_col].dropna())
                ax.set_title(f"Box Plot of {x_col}")
                ax.set_ylabel(x_col)

            elif chart_type == "Pie Chart":
                # Use X column for categories, count them
                counts = self.df[x_col].value_counts()
                if len(counts) > 20:
                     QMessageBox.warning(self, "Warning", "Too many categories for Pie Chart. Showing top 10.")
                     counts = counts.head(10)
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
                ax.set_title(f"Distribution of {x_col}")

            elif chart_type == "Area Chart":
                if not pd.api.types.is_numeric_dtype(self.df[y_col]):
                    raise ValueError(f"Column '{y_col}' must be numeric for Area Chart.")
                plot_df = self.df.sort_values(by=x_col)
                ax.fill_between(plot_df[x_col], plot_df[y_col], alpha=0.5)
                ax.plot(plot_df[x_col], plot_df[y_col])
                ax.set_title(f"{y_col} Area over {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

            elif chart_type == "Hexbin Plot":
                if not pd.api.types.is_numeric_dtype(self.df[x_col]) or not pd.api.types.is_numeric_dtype(self.df[y_col]):
                    raise ValueError("Both columns must be numeric for Hexbin Plot.")
                hb = ax.hexbin(self.df[x_col], self.df[y_col], gridsize=20, cmap='Blues')
                self.figure.colorbar(hb, ax=ax, label='Count')
                ax.set_title(f"Hexbin of {x_col} vs {y_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

            elif chart_type == "Violin Plot":
                # Violin of Y grouped by X
                if not pd.api.types.is_numeric_dtype(self.df[y_col]):
                     raise ValueError(f"Column '{y_col}' must be numeric for Violin Plot.")
                
                groups = self.df.groupby(x_col)[y_col]
                # Prepare data
                data_to_plot = []
                labels = []
                for name, group in groups:
                    data_to_plot.append(group.dropna().values)
                    labels.append(str(name))
                
                if len(labels) > 20:
                     QMessageBox.information(self, "Warning", "Too many groups for Violin Plot. Showing top 10.")
                     data_to_plot = data_to_plot[:10]
                     labels = labels[:10]

                if not data_to_plot:
                    raise ValueError("No data to plot.")

                ax.violinplot(data_to_plot, showmeans=True)
                ax.set_xticks(range(1, len(labels) + 1))
                ax.set_xticklabels(labels, rotation=45)
                ax.set_title(f"Violin Plot of {y_col} by {x_col}")
                ax.set_ylabel(y_col)
                ax.set_xlabel(x_col)

            elif chart_type == "Correlation Heatmap":
                numeric_df = self.df.select_dtypes(include=['number'])
                if numeric_df.empty:
                    raise ValueError("No numeric columns for Correlation Heatmap.")
                corr = numeric_df.corr()
                im = ax.imshow(corr, cmap='coolwarm', interpolation='nearest')
                self.figure.colorbar(im, ax=ax)
                ax.set_xticks(range(len(corr.columns)))
                ax.set_yticks(range(len(corr.columns)))
                ax.set_xticklabels(corr.columns, rotation=45)
                ax.set_yticklabels(corr.columns)
                ax.set_title("Correlation Heatmap")
                # Add annotations (limit if too large)
                if len(corr.columns) < 15:
                    for i in range(len(corr.columns)):
                        for j in range(len(corr.columns)):
                            text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                                           ha="center", va="center", color="black", fontsize=8)

            elif chart_type == "Geo Scatter Plot":
                if not pd.api.types.is_numeric_dtype(self.df[x_col]) or not pd.api.types.is_numeric_dtype(self.df[y_col]):
                    raise ValueError("Longitude (X) and Latitude (Y) columns must be numeric.")
                
                # Scatter plot for map coordinates
                sc = ax.scatter(self.df[x_col], self.df[y_col], alpha=0.6, s=10, c='steelblue')
                ax.set_title(f"Geo Scatter Plot: {y_col} vs {x_col}")
                ax.set_xlabel(f"Longitude ({x_col})")
                ax.set_ylabel(f"Latitude ({y_col})")
                
                # Set aspect ratio to 'equal' for correct map projection approximation
                ax.set_aspect('equal')
                ax.grid(True, linestyle='--', alpha=0.5)

            elif chart_type == "Choropleth Map":
                # Load GeoJSON
                geojson_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "world-countries.json")
                if not os.path.exists(geojson_path):
                    raise FileNotFoundError("World GeoJSON file not found.")
                
                with open(geojson_path, 'r', encoding='utf-8') as f:
                    world_data = json.load(f)

                # Prepare data mapping
                # Assuming X column contains country names/codes, Y column contains numeric values
                if not pd.api.types.is_numeric_dtype(self.df[y_col]):
                    raise ValueError(f"Value column '{y_col}' must be numeric.")

                data_map = dict(zip(self.df[x_col].astype(str), self.df[y_col]))
                
                # Get value range for colormap
                min_val = self.df[y_col].min()
                max_val = self.df[y_col].max()
                norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
                cmap = cm.get_cmap('viridis')

                patches = []
                colors = []

                for feature in world_data['features']:
                    country_name = feature['properties']['name']
                    # Check for match (simple exact match for now, maybe fuzzy later?)
                    # Also try checking ID or other properties if available
                    val = data_map.get(country_name)
                    
                    if val is not None:
                        color = cmap(norm(val))
                    else:
                        color = (0.9, 0.9, 0.9, 1.0) # Grey for no data

                    # Handle Polygon and MultiPolygon
                    geom_type = feature['geometry']['type']
                    coords = feature['geometry']['coordinates']

                    if geom_type == 'Polygon':
                        poly = Polygon(coords[0], closed=True)
                        patches.append(poly)
                        colors.append(color)
                    elif geom_type == 'MultiPolygon':
                        for part in coords:
                            poly = Polygon(part[0], closed=True)
                            patches.append(poly)
                            colors.append(color)

                # Create PatchCollection
                p = PatchCollection(patches, facecolors=colors, edgecolors='white', linewidths=0.5)
                ax.add_collection(p)
                
                # Create colorbar
                sm = cm.ScalarMappable(norm=norm, cmap=cmap)
                sm.set_array([])
                self.figure.colorbar(sm, ax=ax, label=y_col)

                ax.set_title(f"Choropleth Map: {y_col} by {x_col}")
                ax.autoscale_view()
                ax.set_aspect('equal')
                ax.axis('off')

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Plot Error", f"Could not plot data: {str(e)}")
