# Set the file path
file_path <- "file007.txt"  # Replace with the actual path to your file

# Initialize a vector to store timestamps
timestamps <- numeric()

# Read the file line by line
lines <- readLines(file_path)
for (line in lines) {
  if (startsWith(line, "*")) {
    # Extract the timestamp after the asterisk
    timestamp <- as.numeric(sub("^\\*(\\d+).*", "\\1", line))
    timestamps <- c(timestamps, timestamp)
  }
}

# Print the extracted timestamps
print(timestamps)

# Calculate the differences between consecutive timestamps
timestamp_diffs <- diff(timestamps)

# Create a plot
plot(1:(length(timestamp_diffs)+1), timestamps, type = "o", 
     xlab = "Timestamp Index", ylab = "Timestamp",
     main = "Consistency of Timestamp Intervals")

