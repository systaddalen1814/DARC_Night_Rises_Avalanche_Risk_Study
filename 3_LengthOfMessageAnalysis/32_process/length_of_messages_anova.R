library(tidyverse)
library(stringr)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/3_LengthOfMessageAnalysis")
file_list <- list.files(path = "31_input", pattern = "\\.csv$", full.names = TRUE)

# Define common stopwords to remove
stopwords <- scan("../2_DataCombination/24_product/stopwords.txt", what = character(), sep = "\n")

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
    #mutate(Cleaned_Message = map_chr(Message, remove_stopwords, stopwords))
    mutate(Cleaned_Message = Message)
  
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
  
  # Fit a one-way-anova to detect differences in message length
  lm1 <- lm(data = tempdata_df, formula = Message_Length ~ Source)
  print(anova(lm1)) # Show an ANOVA summary
  # Check model assumptions
  par(mfrow=c(2,2))
  print(plot(lm1))
  
  ## Run a Tukey's HSD to find out which sources are different from each other?
  
  # Fit a one-way-anova to detect differences in average word length
  lm2 <- lm(data = tempdata_df, formula = Avg_Word_Length ~ Source)
  print(anova(lm2)) # Show an ANOVA summary
  # Check model assumptions
  par(mfrow=c(2,2))
  print(plot(lm2))
  
  ## Run a Tukey's HSD to find out which sources are different from each other?
  
}
