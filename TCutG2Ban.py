import sys
import re

def cut_to_ban(input_file):
    try:
        # Open the input file in read mode
        with open(input_file, 'r') as file:
            extracted_data = []  # List to store extracted (x, y) pairs
            
            # Iterate through each line in the file
            for line in file:
                # Use regular expression to find pattern of interest
                match = re.search(r'cutg->SetPoint\((\d+),(\d+\.\d+),(\d+\.\d+)\);', line.strip())
                
                # If pattern is found, extract the last two doubles
                if match:
                    point_number = int(match.group(1))
                    x_value = float(match.group(2))
                    y_value = float(match.group(3))
                    
                    # Append (x, y) pair to extracted_data list
                    extracted_data.append((point_number, x_value, y_value))
            
            # Create output filename based on input filename
            output_filename = input_file.replace('.C', '.ban')
            
            # Open the output file in write mode
            with open(output_filename, 'w') as output_file:
                # Write extracted (point_number, x, y) pairs to the output file
                for point_number, x, y in extracted_data:
                    output_file.write(f"{x}\t{y}\n")  # Write each triplet in a new line
                    
            print(f"Extracted data written to '{output_filename}' successfully.")
            
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python TCutG2Ban.py <input_file1> <input_file2> ...")
        sys.exit(1)
    
    input_files = sys.argv[1:]
    for input_file in input_files:
    	cut_to_ban(input_file)

