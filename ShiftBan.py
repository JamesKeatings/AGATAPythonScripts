import sys

def shift_ban(file_name, constant):
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{file_name}' not found.")
        return

    try:
        with open(file_name, 'w') as f:
            for line in lines:
                parts = line.split()
                if len(parts) == 2:
                    try:
                        first_column = float(parts[0])
                        second_column = float(parts[1]) - constant
                        second_column_rounded = round(second_column, 3)
                        f.write(f"{first_column:.3f} {second_column_rounded:.3f}\n")
                    except ValueError:
                        print("Error: Second column must contain numbers.")
                        return
                else:
                    print("Error: Each line must have two columns separated by whitespace.")
                    return
    except IOError:
        print(f"Error: Unable to write to output file '{file_name}'.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ShiftBan.py <file_name1> <file_name2> ... <constant>")
        sys.exit(1)
    
    file_names = sys.argv[1:-1]
    constant = float(sys.argv[-1])
    
    for file_name in file_names:
        shift_ban(file_name, constant)

