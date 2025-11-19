#this a new R script for Transforming World Bank Dataset to Match Navicat Table Schema
#date: 8.7.2025
#created by: Minsol Cho

# 📁 Set working directory where input and output files are located
setwd("C:/Users/MCho/IFPRI Dropbox/Minsol Cho/healthy_diet_dash/updates")

# 📦 Load required packages
library(readxl)     # For reading Excel files
library(dplyr)      # For data manipulation
library(openxlsx)   # For writing Excel files

# 🧠 Define the main function to convert World Bank Excel data to Navicat format
make_navicat_data <- function(file_path) {
  
  # 🧾 Prompt user to enter indicatorTypeID and unit
  indicatorTypeID <- readline("Enter indicatorTypeID (e.g., 475): ")
  unit <- readline("Enter unit (e.g., Percentage): ")
  
  # 📥 Read the Excel file
  df <- read_excel(file_path)
  
  # 🧹 Define metadata columns to exclude from value column detection
  excluded_fields <- c("Classification Name", "Classification Code", "Country Name", "Country Code", "Time", "Time Code")
  
  # 🔍 Detect the column that contains actual indicator values
  # This includes numeric columns or columns with numeric-like strings
  value_candidates <- c()
  for (colname in names(df)) {
    if (!(colname %in% excluded_fields)) {
      numeric_values <- suppressWarnings(as.numeric(df[[colname]]))
      if (sum(!is.na(numeric_values)) > 0) {
        value_candidates <- c(value_candidates, colname)
      }
    }
  }
  
  # ❗ Stop if no valid value column is found
  if (length(value_candidates) == 0) {
    stop("❌ No numeric column found for indicator values. Please check the Excel file.")
  }
  
  # ✅ Use the first detected value column
  value_col <- value_candidates[1]
  name_EN_value <- value_col
  
  # ✅ Check if required columns exist in the input file
  required_cols <- c("Country Code", "Time", value_col)
  missing_cols <- setdiff(required_cols, names(df))
  if (length(missing_cols) > 0) {
    stop(paste("❌ Missing required columns:", paste(missing_cols, collapse = ", ")))
  }
  
  # 🔄 Rename columns to match Navicat structure
  df <- df %>%
    rename(
      ISO3Code = `Country Code`,
      year = Time,
      value = all_of(value_col)
    )
  
  # 📋 Define the full list of columns required by Navicat
  navicat_cols <- c(
    "phase", "id", "name_EN", "name_ES", "name_FR", "indicatorTypeID", "commodityID",
    "ISO3Code", "subregionID", "continentalregionID", "date", "year", "unit",
    "percentageChangeAlert", "referencePeriod", "frequencyID", "value", "created",
    "lastUpdate", "Notes", "last_sync", "dataSourceID", "percentageChange95Threshold",
    "percentageChange90Threshold", "monthIPC3"
  )
  
  # 🧩 Fill in required fields and convert value to numeric
  df_out <- df %>%
    mutate(
      name_EN = name_EN_value,
      indicatorTypeID = indicatorTypeID,
      unit = unit,
      value = suppressWarnings(as.numeric(value))  # Convert safely
    )
  
  # 🧱 Add missing columns as NA
  for (col in navicat_cols) {
    if (!col %in% names(df_out)) {
      df_out[[col]] <- NA
    }
  }
  
  # 🧼 Remove rows with missing or invalid values
  df_out <- df_out %>%
    filter(!is.na(value), value != "..")
  
  # 📐 Reorder columns to match Navicat structure
  df_out <- df_out %>% select(all_of(navicat_cols))
  
  # 💾 Create a safe filename based on the indicator name
  safe_filename <- gsub("[^A-Za-z0-9_\\-]", "_", name_EN_value)
  output_file <- paste0(safe_filename, "_for_Navicat.xlsx")
  
  # 📤 Save the output as an Excel file
  write.xlsx(df_out, output_file)
  message("✅ Conversion complete: ", output_file)
}

# 📂 Prompt user to select a file and run the conversion
file_path <- file.choose()
make_navicat_data(file_path)


