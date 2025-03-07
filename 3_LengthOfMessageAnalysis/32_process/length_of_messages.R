library(yarrr)
library(tidyverse)
library(stringr)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/3_LengthOfMessageAnalysis")
file_list <- list.files(path = "31_input", pattern = "\\.csv$", full.names = TRUE)

# Define common stopwords to remove
stopwords <- c("the", "of", "and", "a", "an", "at", "to", "in", "is", "it", "you", "that", 
               "he", "was", "for", "on", "are", "as", "with", "his", "they", "there", "than", "I")

# Function to remove stopwords from a given message
remove_stopwords <- function(text, stopwords) {
  words <- unlist(str_split(text, "\\s+"))  # Split into words
  words <- words[!tolower(words) %in% stopwords]  # Remove stopwords
  return(paste(words, collapse = " "))  # Reconstruct sentence
}

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
  
  # Remove stopwords from messages
  tempdata_df <- tempdata_df %>%
    mutate(Cleaned_Message = map_chr(Message, remove_stopwords, stopwords))
  
  # Calculate Message_Length (excluding spaces)
  tempdata_df <- tempdata_df %>% 
    mutate(Message_Length = nchar(gsub(" ", "", Message)))
  
  # Calculate Avg_Word_Length (after stopword removal)
  tempdata_df <- tempdata_df %>%
    mutate(Avg_Word_Length = ifelse(
      str_count(Cleaned_Message, "\\S+") > 0,  # Ensure non-empty message
      nchar(gsub(" ", "", Cleaned_Message)) / str_count(Cleaned_Message, "\\S+"),
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
  
  # Generate pirateplot for Average Word Length (after stopword removal)
  plot_filename2 <- file.path("35_datavis", paste0(file_name, "_avg_word_length_plot.jpeg"))
  
  jpeg(plot_filename2, width = 1280, height = 720, res = 120)  # Open JPEG device
  pirateplot(
    formula = Avg_Word_Length ~ Source,
    data = tempdata_df,
    main = paste("Average Word Length (Excl. Stopwords) -", file_name),
    xlab = "AC Location",
    ylab = "Avg Word Length (Characters per Word)"
  )
  dev.off()  # Close the device
  print(paste("Saved plot:", plot_filename2))
}

print("Processing complete!")
