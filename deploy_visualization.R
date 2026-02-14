# GitHub Pages Setup Script
# This script sets up GitHub Pages for automatic visualization viewing

# Load required libraries
library(rmarkdown)
library(fs)

# Ensure docs directory exists
if (!dir_exists("docs")) {
  dir_create("docs")
}

# Render R Markdown to docs folder
rmarkdown::render(
  "analysis/gps_viz.Rmd",
  output_file = "docs/index.html",
  quiet = TRUE
)

# Copy additional files for GitHub Pages
file_copy("README.md", "docs/README.md")
file_copy("data/output/gps_master.csv", "docs/gps_master.csv")

cat("✅ Visualization rendered to docs/index.html")
cat("📁 Available at: https://tomaszbielNCI.github.io/kml_procesor/")
cat("🔄 GitHub Pages will update automatically within minutes")
cat("📊 Total plots generated:", length(list.files("docs/", pattern = "\\.html$")))
cat("🔗 Direct link to visualization ready for sharing")
