from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os
import tempfile

class VisualizationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()
        self.temp_files = []
        self.current_theme = "dark" # Default
        self.advanced_config = {
            "color": None, "size": None, "size_max": 60, 
            "hover_name": None, "log_x": False, "log_y": False, "z": None
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Controls panel with styling
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        controls_layout.setContentsMargins(8, 8, 8, 8)
        
        chart_label = QLabel("Chart Type:")
        controls_layout.addWidget(chart_label)
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            "Histogram", "Scatter Plot", "Bar Chart", "Line Chart", "Box Plot", 
            "Pie Chart", "Area Chart", "Violin Plot", "Correlation Heatmap",
            "Sunburst Chart", "Treemap", "Scatter 3D", "Line 3D", "Choropleth Map"
        ])
        self.chart_type_combo.currentTextChanged.connect(self.update_column_selectors)
        self.chart_type_combo.setMinimumWidth(120)
        controls_layout.addWidget(self.chart_type_combo)

        x_label_text = QLabel("X Column:")
        self.x_label = x_label_text
        controls_layout.addWidget(x_label_text)
        
        self.x_col_combo = QComboBox()
        self.x_col_combo.setMinimumWidth(100)
        controls_layout.addWidget(self.x_col_combo)

        self.y_label = QLabel("Y Column:")
        controls_layout.addWidget(self.y_label)
        self.y_col_combo = QComboBox()
        self.y_col_combo.setMinimumWidth(100)
        controls_layout.addWidget(self.y_col_combo)

        self.z_label = QLabel("Z Column:")
        controls_layout.addWidget(self.z_label)
        self.z_col_combo = QComboBox()
        self.z_col_combo.setMinimumWidth(100)
        controls_layout.addWidget(self.z_col_combo)

        self.plot_button = QPushButton("▶ Plot")
        self.plot_button.clicked.connect(self.start_plotting)
        self.plot_button.setStyleSheet("font-weight: bold; padding: 5px 15px;")
        controls_layout.addWidget(self.plot_button)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Chart area using WebEngine for Plotly
        self.web_view = QWebEngineView()
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.set_placeholder_text("Select data and click Plot to visualize")
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        
        # Initial state
        self.update_column_selectors()

    def set_placeholder_text(self, text):
        actual_theme = "dark" if self.current_theme in ["dark", "auto"] else "light"
        bg_color = "#1e1e1e" if actual_theme == "dark" else "white"
        text_color = "#888" if actual_theme == "dark" else "#666"
        self.web_view.setHtml(f"<html><body style='background-color: {bg_color}; color: {text_color}; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; margin: 0;'><h2>{text}</h2></body></html>")

    def set_dataframe(self, df):
        self.df = df
        self.update_column_combo_boxes()

    def update_column_combo_boxes(self):
        self.x_col_combo.clear()
        self.y_col_combo.clear()
        self.z_col_combo.clear()
        if not self.df.empty:
            columns = self.df.columns.tolist()
            self.x_col_combo.addItems(columns)
            self.y_col_combo.addItems(columns)
            self.z_col_combo.addItems(columns)

    def update_column_selectors(self):
        chart_type = self.chart_type_combo.currentText()
        
        # Reset labels
        self.x_label.setText("X Column:")
        self.y_label.setText("Y Column:")
        self.z_label.setText("Z Column:")
        
        self.x_label.setVisible(True)
        self.x_col_combo.setVisible(True)
        self.y_label.setVisible(True)
        self.y_col_combo.setVisible(True)
        self.z_label.setVisible(False)
        self.z_col_combo.setVisible(False)

        if chart_type in ["Histogram", "Box Plot", "Pie Chart"]:
            self.y_label.setVisible(False)
            self.y_col_combo.setVisible(False)
        elif chart_type == "Correlation Heatmap":
            self.x_label.setVisible(False)
            self.x_col_combo.setVisible(False)
            self.y_label.setVisible(False)
            self.y_col_combo.setVisible(False)
        elif chart_type == "Choropleth Map":
            self.x_label.setText("Location Col:")
            self.y_label.setText("Value Col:")
        elif chart_type == "Sunburst Chart":
            self.x_label.setText("Path Cols (comma sep):")
            self.y_label.setText("Value Col:")
        elif chart_type in ["Scatter 3D", "Line 3D"]:
            self.z_label.setVisible(True)
            self.z_col_combo.setVisible(True)

    def start_plotting(self):
        if self.df.empty:
            QMessageBox.warning(self, "No Data", "No data to load.")
            return

        # Disable UI and show loading
        self.plot_button.setEnabled(False)
        self.plot_button.setText("⌛ Plotting...")
        self.set_placeholder_text("Generating interactive chart, please wait...")
        
        # We use a singleShot timer to let the UI thread process the "Loading..." update
        # before we hit the heavy plotly generation blocking code.
        QTimer.singleShot(100, self.plot_chart)

    def on_load_finished(self, ok):
        self.plot_button.setEnabled(True)
        self.plot_button.setText("▶ Plot")

    def set_theme(self, theme):
        self.current_theme = theme
        if self.temp_files and not self.df.empty:
            # Re-plot to apply new theme colors
            self.plot_chart()
        elif not self.temp_files:
            self.set_placeholder_text("Select data and click Plot to visualize")

    def set_advanced_config(self, config):
        self.advanced_config = config
        # Auto re-plot if data is present and we've pulsed once
        if self.temp_files and not self.df.empty:
            self.plot_chart()

    def plot_chart(self):
        chart_type = self.chart_type_combo.currentText()
        x_col = self.x_col_combo.currentText()
        y_col = self.y_col_combo.currentText()
        z_col = self.z_col_combo.currentText() if self.z_label.isVisible() else self.advanced_config.get("z")

        try:
            fig = None
            actual_theme = "dark" if self.current_theme in ["dark", "auto"] else "light"
            plotly_theme = "plotly_dark" if actual_theme == "dark" else "plotly"
            bg_color = "#1e1e1e" if actual_theme == "dark" else "white"
            font_color = "white" if actual_theme == "dark" else "#333333"

            # Common arguments from advanced config
            common_kwargs = {
                "template": plotly_theme,
                "color": self.advanced_config.get("color"),
                "hover_name": self.advanced_config.get("hover_name")
            }

            if chart_type == "Histogram":
                fig = px.histogram(self.df, x=x_col, nbins=30, marginal="box", **common_kwargs)
                fig.update_layout(title=f"Histogram of {x_col}")

            elif chart_type == "Scatter Plot":
                fig = px.scatter(self.df, x=x_col, y=y_col, 
                                 size=self.advanced_config.get("size"),
                                 size_max=self.advanced_config.get("size_max"),
                                 log_x=self.advanced_config.get("log_x"),
                                 log_y=self.advanced_config.get("log_y"),
                                 trendline="ols" if pd.api.types.is_numeric_dtype(self.df[x_col]) and pd.api.types.is_numeric_dtype(self.df[y_col]) else None,
                                 **common_kwargs)
                fig.update_layout(title=f"{x_col} vs {y_col}")
            
            elif chart_type == "Scatter 3D":
                if not z_col:
                    raise ValueError("Z Column is required for 3D plots. Set it in Plot Configuration.")
                fig = px.scatter_3d(self.df, x=x_col, y=y_col, z=z_col,
                                    size=self.advanced_config.get("size"),
                                    size_max=self.advanced_config.get("size_max"),
                                    **common_kwargs)
                fig.update_layout(title=f"3D Scatter: {x_col}, {y_col}, {z_col}")

            elif chart_type == "Line 3D":
                if not z_col:
                    raise ValueError("Z Column is required for 3D plots. Set it in Plot Configuration.")
                df_sorted = self.df.sort_values(by=x_col)
                fig = px.line_3d(df_sorted, x=x_col, y=y_col, z=z_col, **common_kwargs)
                fig.update_layout(title=f"3D Line Path")

            elif chart_type == "Bar Chart":
                if len(self.df) > 100:
                    # We only aggregate if color is NOT set, otherwise grouping is complex
                    if not common_kwargs["color"]:
                        df_agg = self.df.groupby(x_col)[y_col].mean().reset_index()
                        fig = px.bar(df_agg, x=x_col, y=y_col, **common_kwargs)
                        fig.update_layout(title=f"Average {y_col} by {x_col} (Aggregated)")
                    else:
                        fig = px.bar(self.df, x=x_col, y=y_col, **common_kwargs)
                else:
                    fig = px.bar(self.df, x=x_col, y=y_col, **common_kwargs)

            elif chart_type == "Line Chart":
                df_sorted = self.df.sort_values(by=x_col)
                fig = px.line(df_sorted, x=x_col, y=y_col, markers=True, 
                              log_x=self.advanced_config.get("log_x"),
                              log_y=self.advanced_config.get("log_y"),
                              **common_kwargs)
                fig.update_layout(title=f"{y_col} over {x_col}")

            elif chart_type == "Box Plot":
                fig = px.box(self.df, y=x_col, points="all", **common_kwargs)
                fig.update_layout(title=f"Box Plot of {x_col}")

            elif chart_type == "Pie Chart":
                fig = px.pie(self.df, names=x_col, values=y_col if y_col != x_col else None, template=plotly_theme) # Pie doesn't support some common kwargs same way
                fig.update_layout(title=f"Distribution of {x_col}")

            elif chart_type == "Area Chart":
                df_sorted = self.df.sort_values(by=x_col)
                fig = px.area(df_sorted, x=x_col, y=y_col, **common_kwargs)
                fig.update_layout(title=f"Area Chart: {y_col} vs {x_col}")

            elif chart_type == "Violin Plot":
                fig = px.violin(self.df, y=y_col, x=x_col, box=True, points="all", **common_kwargs)
                fig.update_layout(title=f"Violin Plot: {y_col} by {x_col}")

            elif chart_type == "Correlation Heatmap":
                numeric_df = self.df.select_dtypes(include=['number'])
                if numeric_df.empty:
                    raise ValueError("No numeric columns for Correlation Heatmap.")
                corr = numeric_df.corr()
                fig = px.imshow(corr, text_auto=True, aspect="auto", template=plotly_theme, color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
                fig.update_layout(title="Correlation Heatmap")

            elif chart_type == "Sunburst Chart":
                paths = [c.strip() for c in x_col.split(',')]
                valid_paths = [p for p in paths if p in self.df.columns]
                if not valid_paths:
                    valid_paths = [x_col]
                fig = px.sunburst(self.df, path=valid_paths, 
                                  values=y_col if pd.api.types.is_numeric_dtype(self.df[y_col]) else None,
                                  color=common_kwargs["color"],
                                  template=plotly_theme)
                fig.update_layout(title="Sunburst Hierarchy")

            elif chart_type == "Treemap":
                paths = [c.strip() for c in x_col.split(',')]
                valid_paths = [p for p in paths if p in self.df.columns]
                if not valid_paths:
                    valid_paths = [x_col]
                fig = px.treemap(self.df, path=valid_paths, 
                                 values=y_col if pd.api.types.is_numeric_dtype(self.df[y_col]) else None,
                                 color=common_kwargs["color"],
                                 template=plotly_theme)
                fig.update_layout(title="Treemap Hierarchy")

            elif chart_type == "Choropleth Map":
                fig = px.choropleth(self.df, locations=x_col, locationmode="country names", color=y_col, template=plotly_theme, color_continuous_scale=px.colors.sequential.Plasma)
                fig.update_layout(title=f"Global distribution of {y_col}")

            if fig:
                fig.update_layout(
                    margin=dict(l=20, r=20, t=60, b=20),
                    paper_bgcolor=bg_color,
                    plot_bgcolor=bg_color,
                    font=dict(color=font_color, size=12)
                )
                
                # Render to HTML - Bundle Plotly.js and force modebar visibility
                config = {'displayModeBar': True, 'responsive': True}
                html = fig.to_html(include_plotlyjs=True, full_html=True, config=config)
                
                # Performance optimization: Inject script to set willReadFrequently=true for 2D canvases
                # This resolves the browser warning and can improve performance for readback operations
                optimization_script = """
                <script>
                (function() {
                    const originalGetContext = HTMLCanvasElement.prototype.getContext;
                    HTMLCanvasElement.prototype.getContext = function(type, attributes) {
                        if (type === '2d') {
                            attributes = attributes || {};
                            attributes.willReadFrequently = true;
                        }
                        return originalGetContext.call(this, type, attributes);
                    };
                })();
                </script>
                """
                if "<body>" in html:
                    html = html.replace("<body>", "<body>" + optimization_script)
                
                fd, path = tempfile.mkstemp(suffix='.html')
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                self.temp_files.append(path)
                self.web_view.setUrl(QUrl.fromLocalFile(path))
            else:
                self.on_load_finished(True)

        except Exception as e:
            QMessageBox.critical(self, "Plot Error", f"Could not plot data: {str(e)}")
            self.plot_button.setEnabled(True)
            self.plot_button.setText("▶ Plot")
            self.set_placeholder_text("An error occurred during plot generation.")

    def closeEvent(self, event):
        # Clean up temporary files
        for path in self.temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
        super().closeEvent(event)
