# GPS Data Processor - Wicklow Mountain Hiking Data

This repository contains a comprehensive system for processing and visualizing GPS data from hiking activities in Wicklow Mountains, Ireland.

## 🎯 Purpose

A complete solution for handling GPS data from various sources (GPX, KML files) collected during hiking trips in Wicklow Mountains. The system provides data transformation, analysis, and advanced visualization capabilities.

## 🛠️ Technologies Used

### Python - Data Processing & Transformation
- **Easy Data Transformations**: Automated conversion between different GPS formats
- **GPX Extensions Support**: Enhanced time data extraction from GPS extensions
- **Batch Processing**: Handle multiple files simultaneously
- **Statistical Analysis**: Comprehensive route statistics and metrics

### R - Advanced Data Visualization
- **ggplot2**: Professional-quality statistical graphics
- **Better Visualizations**: Interactive and publication-ready plots
- **Comprehensive Analysis**: 22 different visualization types
- **Statistical Insights**: Correlation analysis, distribution plots, geographic mapping

## 📊 Features

### Data Processing
- **Multi-format Support**: GPX and KML file processing
- **Time Series Analysis**: Enhanced time extraction from GPX extensions
- **Route Statistics**: Distance, altitude, calories calculation
- **Data Validation**: Complete data integrity checks

### Visualizations
- **Geographic Maps**: GPS point scatter plots and density contours
- **Altitude Analysis**: Histograms, boxplots, and elevation profiles
- **Time-based Analysis**: Speed distributions and temporal patterns
- **Statistical Plots**: Correlation analysis and regression models
- **Route Comparisons**: Multi-route performance metrics

### Special Analysis
- **Anscombe's Quartet**: Advanced statistical analysis for Valleymount to Blessington route
- **Speed Phase Detection**: Walking vs car journey identification
- **Transition Analysis**: Automatic detection of transport mode changes

## 🗂️ Repository Structure

```
├── data/
│   ├── input/          # Raw GPS files (GPX, KML)
│   └── output/         # Processed data and master CSV
├── src/
│   ├── core/           # Core processing modules
│   └── scripts/        # Utility scripts
├── analysis/           # R Markdown visualizations
├── archive/           # Historical analysis scripts
└── docs/             # Documentation
```

## 🚀 Quick Start

### Python Processing
```bash
# Process all GPS files
python src/scripts/gpx_fast_converter.py

# Generate master CSV with enhanced time data
python src/scripts/gpx_fast_converter.py --enhanced-time
```

### R Visualization
```r
# Open in RStudio
file.open("analysis/gps_viz.Rmd")

# Knit to HTML
rmarkdown::render("analysis/gps_viz.Rmd")
```

## 📈 Key Insights

The system provides comprehensive analysis of hiking data including:
- **Route Performance**: Distance vs calories correlation
- **Elevation Profiles**: Altitude changes throughout routes
- **Speed Analysis**: Walking vs car journey detection
- **Geographic Patterns**: Density analysis of hiking areas
- **Temporal Trends**: Time-based activity patterns

## 🏔️ Focus Area: Wicklow Mountains

Specifically designed for analyzing hiking data from:
- **Wicklow Mountains National Park**
- **Glendalough Valley**
- **Scarr Mountain** routes
- **Valleymount to Blessington** trails
- **Gateway to Wicklow Gap** paths

## 📊 Visualization Gallery

The system generates 22 different types of visualizations:

1. **Altitude Analysis**: Histograms, distributions, boxplots
2. **Geographic Mapping**: Scatter plots, density contours
3. **Time Series**: Speed analysis, temporal patterns
4. **Statistical Analysis**: Correlation, regression, quartets
5. **Route Comparisons**: Multi-route performance metrics

## 🔧 Data Enhancement

- **GPX Extensions**: Extract detailed time data (clock, seconds)
- **Route Metadata**: Complete statistics for each trail
- **Quality Validation**: Data integrity and completeness checks
- **Format Standardization**: Unified data structure across sources

## 📝️ Usage Examples

### Basic Processing
```python
from src.core.processor import GPSProcessor

processor = GPSProcessor()
data = processor.process_files("data/input/")
data.save_master_csv("data/output/gps_master.csv")
```

### Advanced Visualization
```r
# Load processed data
gps_data <- read_csv("../data/output/gps_master.csv")

# Create altitude distribution
ggplot(gps_data, aes(x = altitude)) +
  geom_histogram(bins = 50, fill = "skyblue") +
  labs(title = "Wicklow Mountains - Altitude Distribution")
```

## 🎯 Key Benefits

- **Easy Data Transformations**: Python handles complex GPS format conversions
- **Better Visualizations**: R/ggplot2 creates professional statistical graphics
- **Comprehensive Analysis**: Complete end-to-end data pipeline
- **Wicklow Specific**: Tailored for Irish mountain hiking data
- **Research Ready**: Suitable for academic or recreational analysis

## 📚 Dependencies

### Python
- pandas, numpy, gpxpy, xml.etree.ElementTree
- matplotlib, seaborn for basic plotting

### R
- tidyverse, ggplot2, lubridate
- DT, kableExtra for tables
- rmarkdown for reports

---

**Perfect for hikers, researchers, and data enthusiasts exploring the beautiful Wicklow Mountains!**
