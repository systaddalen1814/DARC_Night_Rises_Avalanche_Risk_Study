library(tidyverse)
library(ggplot2)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/2_DataCombination")

# Get the list of files, excluding those with "master" in the filename
file_list <- list.files(path = "24_product", pattern = "\\.csv$", full.names = TRUE)
file_list <- file_list[!grepl("master", tolower(file_list))]  # Exclude "master" files

# Define custom order and labels
risk_levels <- c("low", "moderate", "considerable", "high", "extreme")
custom_labels <- c("Low Risk", "Moderate Risk", "Considerable Risk", "High Risk", "Extreme Risk")

# Create an empty dataframe to store counts
file_counts <- data.frame(Risk_Level = character(), Observations = integer(), stringsAsFactors = FALSE)

for (file in file_list) {
  file_name <- tolower(basename(file))  # Convert filename to lowercase for matching
  df <- read_csv(file)
  
  # Determine the risk level based on filename
  matched_level <- risk_levels[sapply(risk_levels, function(x) grepl(x, file_name))]
  
  if (length(matched_level) == 1) {  # Ensure only one match
    file_counts <- rbind(file_counts, data.frame(Risk_Level = matched_level, Observations = nrow(df)))
  } else {
    print(paste("Skipping", file_name, "- no clear risk level found."))
  }
}

# Convert Risk_Level to a factor with a predefined order
file_counts$Risk_Level <- factor(file_counts$Risk_Level, levels = risk_levels, labels = custom_labels)

# Create a bar plot with custom order and labels
p <- ggplot(file_counts, aes(x = Risk_Level, y = Observations, fill = Risk_Level)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = Observations), vjust = c(2,2,2,2,-0.5), size = 5, fontface = "bold") +  # Add count annotations
  scale_fill_manual(values = c("lightblue", "gold", "orange", "red", "darkred")) +  # Custom colors
  theme_minimal() +
  labs(title = "Total Observations by Avalanche Risk Level", x = "Risk Level", y = "Number of Observations") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate labels for readability

# Save the plot
plot_filename <- "25_datavis/observation_counts.jpeg"
ggsave(filename = plot_filename, plot = p, width = 10, height = 6, dpi = 300)

print(paste("Saved total observations plot:", plot_filename))
