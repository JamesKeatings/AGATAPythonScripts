import sys
import re

def ban_to_cut(input_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    output_file = input_file.replace(".ban", ".C")
    cut_name = input_file.replace(".ban","")
    match = re.match(r"mas_ban_(\d+)_(\d+)", cut_name)
    if match:
        Z = match.group(1)
        M = match.group(2)
        reformatted_name = f"z{Z}m{M}"
    try:
        with open(output_file, 'w') as of:
            i = 0
            of.write("{\n")
            of.write(f"\n\tTCutG *{cut_name} = new TCutG(\"{reformatted_name}\",{len(lines)});")
            of.write(f"\n\t{cut_name}->SetVarX(\"\");")
            of.write(f"\n\t{cut_name}->SetVarY(\"\");")
            of.write(f"\n\t{cut_name}->SetTitle(\"Graph\");")
            of.write(f"\n\t{cut_name}->SetLineColor(2);")
            of.write(f"\n\t{cut_name}->SetLineWidth(3);\n") 
            for line in lines:
                parts = line.split()
                if len(parts) == 2:
                    try:
                        first_column = float(parts[0])
                        second_column = float(parts[1])
                        of.write(f"\t{cut_name}->SetPoint({i},{first_column:.3f},{second_column:.3f});\n")
                        i=i+1
                    except ValueError:
                        print("Error: Second column must contain numbers.")
                        return
                else:
                    print("Error: Each line must have two columns separated by whitespace.")
                    return
            of.write(f"\t{cut_name}->Draw(\"SAME\");")
            of.write("\n}")
    except IOError:
        print(f"Error: Unable to write to output file '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Ban2TCutG.py <input_file1> <input_file2> ...")
        sys.exit(1)
    
    input_files = sys.argv[1:]
    for input_file in input_files:
    	ban_to_cut(input_file)
