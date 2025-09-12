import csv
import hashlib
import os

# --- Method 1: Human-Readable Code Generation ---
def generate_readable_code(id1, id2, name):
    """
    Generates a human-readable unique code from candidate data.
    Example: 'WEI Zhuolun', 'N25302312', '25233610' -> 'WZ-2312-3610'
    """
    try:
        name_parts = name.strip().split()
        initials = "".join([part[0] for part in name_parts]).upper()
        last4_id1 = id1.strip()[-4:]
        last4_id2 = id2.strip()[-4:]
        return f"{initials}-{last4_id1}-{last4_id2}"
    except IndexError:
        # Handle cases with empty names or IDs
        return "INVALID-DATA"

# --- Method 2: Hash-Based Code Generation ---
def generate_hash_code(id1, id2, name, length=10):
    """
    Generates a unique hash-based code from candidate data using SHA-256.
    """
    # Combine data into a single, consistent string
    combined_string = f"{id1.strip()}-{id2.strip()}-{name.strip().replace(' ', '')}"
    
    # Encode the string to bytes and create a hash
    encoded_string = combined_string.encode('utf-8')
    hasher = hashlib.sha256(encoded_string)
    
    # Return the first `length` characters of the hexadecimal hash
    return hasher.hexdigest()[:length]

# --- Main Processing Logic ---
def process_student_data(input_file, output_file):
    """
    Reads student data, generates codes, and writes to a CSV file.
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Please make sure the data file is in the same directory as the script.")
        return

    # Prepare data for CSV writing
    processed_data = []
    header = ['ID1', 'ID2', 'Name', 'Readable_Code', 'Hash_Code']
    processed_data.append(header)

    print(f"Reading data from '{input_file}'...")

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            # Skip empty or blank lines
            if not line.strip():
                continue
            
            # Split the line by tabs
            parts = line.strip().split('\t')
            
            if len(parts) == 3:
                id1, id2, name = parts
                
                # Generate both types of codes
                readable_code = generate_readable_code(id1, id2, name)
                hash_code = generate_hash_code(id1, id2, name)
                
                # Add the complete row to our data list
                processed_data.append([id1, id2, name, readable_code, hash_code])
            else:
                print(f"Warning: Skipping malformed line: {line.strip()}")

    # Write the processed data to the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(processed_data)

    print(f"\nProcessing complete!")
    print(f"Output successfully saved to '{output_file}'.")

# --- Script Execution ---
if __name__ == "__main__":
    # Define the input and output filenames
    input_filename = "student data.md"
    output_filename = "student_codes.csv"
    
    # Run the main processing function
    process_student_data(input_filename, output_filename)
