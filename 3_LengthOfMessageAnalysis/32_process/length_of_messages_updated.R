library(yarrr)
library(tidyverse)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/3_LengthOfMessageAnalysis")
file_list <- list.files(path = "31_input", pattern = "\\.csv$", full.names = TRUE)

# Loop through each CSV file
for (file in file_list) {
  file_name <- tools::file_path_sans_ext(basename(file))
  
  # Read CSV file
  tempdata_df <- read_csv(file)
  print(paste("Processing file:", file_name))
  
  # Skip empty data frames
  if (nrow(tempdata_df) == 0) {
    print(paste("Skipping", file_name, "because the data frame is empty"))
    next
  }
  
  # Check if required columns exist
  if (!all(c("Message", "Source") %in% colnames(tempdata_df))) {
    print(paste("Skipping", file_name, "due to missing required columns"))
    next
  }
  
  # Calculate Message_Length (excluding spaces)
  tempdata_df <- tempdata_df %>% 
    mutate(Message_Length = nchar(gsub(" ", "", Message)))
  
  # Calculate Avg_Word_Length
  tempdata_df <- tempdata_df %>%
    mutate(Avg_Word_Length = ifelse(
      str_count(Message, "\\S+") > 0,  # Check if there are words
      Message_Length / str_count(Message, "\\S+"),  # Divide by word count
      NA  # Avoid division by zero
    ))
  
  # Generate pirateplot for Message Length
  plot_filename1 <- file.path("35_datavis", paste0(file_name, "_length_plot.jpeg"))
  
  jpeg(plot_filename1, width = 1280, height = 720, res = 120)  # Open JPEG device
  pirateplot(
    formula = Message_Length ~ Source,
    data = tempdata_df,
    main = paste("Length of Message by Location -", file_name),
    xlab = "AC Location",
    ylab = "Message Length (Num Characters)"
  )
  dev.off()  # Close the device
  print(paste("Saved plot:", plot_filename1))
  
  # Generate pirateplot for Average Word Length
  plot_filename2 <- file.path("35_datavis", paste0(file_name, "_avg_word_length_plot.jpeg"))
  
  jpeg(plot_filename2, width = 1280, height = 720, res = 120)  # Open JPEG device
  pirateplot(
    formula = Avg_Word_Length ~ Source,
    data = tempdata_df,
    main = paste("Average Word Length by Location -", file_name),
    xlab = "AC Location",
    ylab = "Avg Word Length (Characters per Word)"
  )
  dev.off()  # Close the device
  print(paste("Saved plot:", plot_filename2))
}

print("Processing complete!")
