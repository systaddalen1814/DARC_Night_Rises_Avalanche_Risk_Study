import os
import pandas as pd

def remove_duplicate_message(message_original):
    """
    Removes duplicate sentences if they occur exactly twice.
    Also removes newline characters and extra spaces and periods
    """
    message = message_original  # Store original message for comparison

    # Remove newline characters and extra spaces
    message = message.replace('\n', ' ').strip()

    # Split the message into individual sentences
    sentences = message.split(". ")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Remove all periods from the sentences
    sentences = [sentence.replace('.', '') for sentence in sentences]

    # Count occurrences of each sentence
    sentence_count = {}
    for sentence in sentences:
        sentence_lower = sentence.lower()  # Case insensitive
        sentence_count[sentence_lower] = sentence_count.get(sentence_lower, 0) + 1

    # If all sentences occur exactly twice, deduplicate them
    if all(count == 2 for count in sentence_count.values()):
        unique_sentences = list(sentence_count.keys())
        return ". ".join(unique_sentences) + "." if unique_sentences else ""
    else:
        return message_original  # Return original if not all are duplicated

def remove_full_message_duplicates(src_folder, dest_folder, file_name_to_process=0):
    """
    Reads CSV files in the source folder, checks if the 'Message' column contains 
    fully duplicated sentences, and reduces them to a single instance if all sentences appear exactly twice.
    
    If file_name_to_process is set to 0, it processes all CSV files in the folder.
    """
    
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Get list of files to process
    files_to_process = [file_name_to_process] if file_name_to_process != 0 else [
        f for f in os.listdir(src_folder) if f.lower().endswith(".csv")
    ]

    for file_name in files_to_process:
        src_file = os.path.join(src_folder, file_name)

        try:
            if os.path.isfile(src_file):
                df = pd.read_csv(src_file)

                # Ensure 'Message' column exists
                if 'Message' in df.columns:
                    # Apply the function to the 'Message' column
                    df['Message'] = df['Message'].apply(remove_duplicate_message)

                    # Save the cleaned file
                    dest_file = os.path.join(dest_folder, file_name)
                    df.to_csv(dest_file, index=False)
                    print(f"Fixed & saved: {file_name}")

                else:
                    print(f"Skipping {file_name} - 'Message' column not found.")

            else:
                print(f"File {file_name} not found or not a CSV.")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    print("\nDuplicate sentence removal completed.")

# Define source and destination folders
source_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")  # Adjust based on your folder structure
destination_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")  # Adjust as needed

# Set to 0 to process all files, or specify a file name
file_name_to_process = 0  # Change to a specific file name if needed

remove_full_message_duplicates(source_folder, destination_folder, file_name_to_process)
