library(yarrr)
library(tidyverse)

setwd("~/Desktop/Spring 2025/Capstone/DARC_Night_Rises_Avalanche_Risk_Study/3_LengthOfMessageAnalysis")

dat <- read_csv("31_input/Master_Avalanche_Data.csv")

dat <- dat %>% 
  mutate(Message_Length = nchar(gsub(" ", "", Message)))

pirateplot(
  data = dat,
  formula = Message_Length ~ Source,
  main = "Length of Message by Location",
  xlab = "AC Location",
  ylab = "Message Length (Num Characters)"
)


