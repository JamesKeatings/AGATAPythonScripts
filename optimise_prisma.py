import re
import subprocess
import os
import shutil

# Set your step values for each loop
quad_length_step = 5
dipole_angle_step = 1
dipole_exit_angle_step = 1
target_quad_distance_step = 5
target_dipole_distance_step = 10

# Set your minimum and maximum values for the first loop
min_quad_length = 350
max_quad_length = 380

# Set your minimum and maximum values for the second loop
min_dipole_angle = 26
max_dipole_angle = 26

# Set your minimum and maximum values for the third loop
min_dipole_exit_angle = 131
max_dipole_exit_angle = 131

# Set your minimum and maximum values for the fourth loop
min_target_quad_distance = 545
max_target_quad_distance = 545

# Set your minimum and maximum values for the fifth loop
min_target_dipole_distance = 1600
max_target_dipole_distance = 1600

# Loop through the desired range of values for quad_length
for current_quad_length in range(
    min_quad_length, max_quad_length + 1, quad_length_step
):
    # Loop through the desired range of values for dipole_entrance_angle
    for current_dipole_angle in range(
        min_dipole_angle, max_dipole_angle + 1, dipole_angle_step
    ):
        # Loop through the desired range of values for dipole_exit_angle
        for current_dipole_exit_angle in range(
            min_dipole_exit_angle, max_dipole_exit_angle + 1, dipole_exit_angle_step
        ):
            # Loop through the desired range of values for target_quad_distance
            for current_target_quad_distance in range(
                min_target_quad_distance,
                max_target_quad_distance + 1,
                target_quad_distance_step,
            ):
                # Loop through the desired range of values for target_dipole_distance
                for current_target_dipole_distance in range(
                    min_target_dipole_distance,
                    max_target_dipole_distance + 1,
                    target_dipole_distance_step,
                ):
                    # Create the file path
                    file_path = "PrismaConf/solver.conf"

                    # Open the file and read its content
                    with open(file_path, "r") as file:
                        lines = file.readlines()

                    # Use regex to find and modify the line for quad_length
                    quad_length_pattern = re.compile(r"^quad_length = ")
                    for i, line in enumerate(lines):
                        if quad_length_pattern.match(line):
                            lines[i] = f"quad_length = {current_quad_length}\n"
                            break

                    # Use regex to find and modify the line for dipole_entrance_angle
                    dipole_angle_pattern = re.compile(r"^dipole_entrance_angle = ")
                    for i, line in enumerate(lines):
                        if dipole_angle_pattern.match(line):
                            lines[i] = (
                                f"dipole_entrance_angle = {current_dipole_angle}.\n"
                            )
                            break

                    # Use regex to find and modify the line for dipole_exit_angle
                    dipole_exit_angle_pattern = re.compile(r"^dipole_exit_angle = ")
                    for i, line in enumerate(lines):
                        if dipole_exit_angle_pattern.match(line):
                            lines[i] = (
                                f"dipole_exit_angle = {current_dipole_exit_angle}.0\n"
                            )
                            break

                    # Use regex to find and modify the line for target_quad_distance
                    target_quad_distance_pattern = re.compile(
                        r"^target_quad_distance = "
                    )
                    for i, line in enumerate(lines):
                        if target_quad_distance_pattern.match(line):
                            lines[i] = (
                                f"target_quad_distance = {current_target_quad_distance}\n"
                            )
                            break

                    # Use regex to find and modify the line for target_dipole_distance
                    target_dipole_distance_pattern = re.compile(
                        r"^target_dipole_distance = "
                    )
                    for i, line in enumerate(lines):
                        if target_dipole_distance_pattern.match(line):
                            lines[i] = (
                                f"target_dipole_distance = {current_target_dipole_distance}.\n"
                            )
                            break

                    # Write the modified content back to the file
                    with open(file_path, "w") as file:
                        file.writelines(lines)

                    # Run the bash script "RunSelector"
                    subprocess.run(
                        [
                            "./RunAnalysis",
                            "20",
                            "--mode",
                            "1",
                            "--nrevts",
                            "3000000",
                            "--nrthr",
                            "7",
                        ]
                    )
                    subprocess.run(
                        ["./RunAnalysis", "20", "--mode", "2", "--nrthr", "2"]
                    )
                    # Move the "out.root" file and add current values to the filename
                    # original_out_file = 'Out/run_0020_0000.root'
                    # new_out_file = f'Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/'
                    subprocess.run(
                        [
                            "mkdir",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0000.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0000.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0001.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0001.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0002.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0002.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0003.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0003.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0004.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0004.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0005.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0005.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/run_0020_0006.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/run_0020_0006.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "mv",
                            "Out/sum-20_7.root",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/sum-20_7.root",
                        ]
                    )
                    subprocess.run(
                        [
                            "cp",
                            "PrismaConf/solver.conf",
                            f"Out/results_run_0020_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}/",
                        ]
                    )
        # Example usage:
        # source_directory = 'Runs/run_0046/filterFiles/'
        # destination_directory = 'Runs/run_0046_{current_quad_length}_{current_dipole_angle}_{current_dipole_exit_angle}_{current_target_quad_distance}_{current_target_dipole_distance}'
        # subprocess.run(["cp", "-r", source_directory, destination_directory])
