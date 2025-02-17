library(tidyverse)
library(naniar)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/0_WebScraper")

file_list <- list.files(path = "04_product", pattern = "\\.csv$", full.names = TRUE)

for (file in file_list) {
  file_name <- tools::file_path_sans_ext(basename(file))
  assign(paste0("data_", file_name), read_csv(file), envir = .GlobalEnv)
  print(paste("Processing file:", file))
}


data_vars <- ls(pattern = "^data_")
for (var in data_vars) {
  print(paste("Processing missing value plot for:", var))
  
  p <- vis_miss(get(var)) + ggtitle(paste("Missing Values in", var))
  
  plot_filename <- file.path("05_datavis", paste0(var, "_missing_plot.jpeg"))
  
  ggsave(filename = plot_filename, plot = p, width = 8, height = 6, dpi = 300)
  
  print(paste("Saved plot:", plot_filename))
}
