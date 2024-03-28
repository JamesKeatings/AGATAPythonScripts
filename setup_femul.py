import glob
import os
import subprocess
import sys
from datetime import datetime


class colours:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


def setup_femul(run_number):
    # Initialize source_folder_path outside the if block
    source_folder_path = None
    gen_conf_number = 0
    aoverq_number = 0

    # DEFINE VARIABLES
    source_folder_pattern = (
        f"/media/jk/data_agata_0/AGATAD_P2_EXP_013/run_{run_number:04d}_*/"
    )
    destination_folder_path = f"run_{run_number:04d}/"
    conf_folder_pattern = f"Conf"
    data_folder_pattern = f"Data"
    topology_file_pattern = f"Template/Topology_FromPSAToTreePRISMA.conf"
    prismaconf_folder_pattern = f"Template/PrismaConf"

    # SET FLAGS FOR ANALYSIS
    do_setup = True
    do_genconf = False
    do_femul = False

    # CODE STARTS HERE
    source_folder_paths = glob.glob(source_folder_pattern)
    current_directory = os.getcwd()

    log_path = current_directory + "/LOG_setup_femul.log"

    current_datetime = datetime.now()
    with open(log_path, "a") as file:
        file.write(f"run_{run_number:04d}" + "\n")
        file.write(
            "Start time:\t" + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        )

    folder = False
    conf = False
    genconf = False
    aoverq = False
    prismaconf = False
    data = False
    prismadata = False

    if do_setup:
        # CHECK FOR AND CREATE RUN_ DIRECTORY
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)
            print(
                f"Folder {destination_folder_path} created {colours.GREEN}successfully{colours.END}."
            )
            folder = True

        # COPY TOPOLOGY
        try:
            subprocess.run(
                ["cp", topology_file_pattern, destination_folder_path], check=True
            )
            print(
                f"Topology copied {colours.GREEN}successfully{colours.END} for file: {topology_file_pattern} to {destination_folder_path}"
            )
            topology = True
        except subprocess.CalledProcessError as e:
            print(f"{colours.RED}Error{colours.END} copying topology: {e}")

        # COPY CONF FOLDER
        if source_folder_paths:
            source_folder_path = source_folder_paths[
                0
            ]  # Update the value inside the if block
            try:
                subprocess.run(
                    [
                        "cp",
                        "-r",
                        source_folder_path + conf_folder_pattern,
                        destination_folder_path,
                    ],
                    check=True,
                )
                print(
                    f"Conf/ folder copied {colours.GREEN}successfully{colours.END} for folder: {source_folder_path+conf_folder_pattern} to {destination_folder_path}"
                )
                conf = True
            except subprocess.CalledProcessError as e:
                print(f"{colours.RED}Error{colours.END} copying for folder: {e}")

        # COPY GEN_CONF.PY
        if 46 <= run_number <= 50:
            gen_conf_number = 46
        elif 42 <= run_number <= 45:
            gen_conf_number = 42
        elif 40 <= run_number <= 41:
            gen_conf_number = 40
        elif 32 <= run_number <= 39:
            gen_conf_number = 32
        elif 30 <= run_number <= 31:
            gen_conf_number = 30
        elif 26 <= run_number <= 29:
            gen_conf_number = 26
        elif 23 <= run_number <= 25:
            gen_conf_number = 23
        elif 20 <= run_number <= 22:
            gen_conf_number = 20
        elif run_number == 19:
            gen_conf_number = 19
        elif 7 <= run_number <= 18:
            gen_conf_number = 7

        try:
            genconf_file_path = f"Template/gen_conf_run_{gen_conf_number:04d}.py"
            subprocess.run(
                ["cp", genconf_file_path, destination_folder_path + "/gen_conf.py"],
                check=True,
            )
            print(
                f"gen_conf.py copied {colours.GREEN}successfully{colours.END} for file: {genconf_file_path} to {destination_folder_path}"
            )
            genconf = True
        except subprocess.CalledProcessError as e:
            print(f"{colours.RED}Error{colours.END} copying genconf: {e}")

        # COPY UPDATED PRISMACONF FOLDER INTO RUN_*/CONF/PRISMA
        if conf:
            try:
                subprocess.run(
                    [
                        "cp",
                        "-r",
                        prismaconf_folder_pattern,
                        destination_folder_path + conf_folder_pattern + "/prisma",
                    ],
                    check=True,
                )
                print(
                    f"PrismaConf folder copied {colours.GREEN}successfully{colours.END} for file: {prismaconf_folder_pattern} to {destination_folder_path+conf_folder_pattern}/prisma"
                )
                prismaconf = True
            except subprocess.CalledProcessError as e:
                print(f"{colours.RED}Error{colours.END} copying PrismaConf: {e}")

        # COPY A_OVER_Q.CAL
        if conf and prismaconf:
            if run_number == 50:
                aoverq_number = 50
            elif 45 <= run_number <= 49:
                aoverq_number = 45
            elif run_number == 44:
                aoverq_number = 44
            elif 39 <= run_number <= 43:
                aoverq_number = 39
            elif run_number == 37:
                aoverq_number = 37
            elif run_number == 36:
                aoverq_number = 36
            elif 31 <= run_number <= 34:
                aoverq_number = 31
            elif 8 <= run_number <= 30:
                aoverq_number = 16

            try:
                aoverq_file_path = (
                    f"Template/a_over_q/a_over_q_run_{aoverq_number:04d}.cal"
                )
                subprocess.run(
                    ["rm", destination_folder_path + "Conf/prisma/cal/a_over_q.cal"],
                    check=True,
                )
                subprocess.run(
                    [
                        "cp",
                        aoverq_file_path,
                        destination_folder_path + "Conf/prisma/cal/a_over_q.cal",
                    ],
                    check=True,
                )
                print(
                    f"a_over_q.cal copied {colours.GREEN}successfully{colours.END} for file: {aoverq_file_path} to {destination_folder_path}/Conf/prisma/cal"
                )
                aoverq = True
            except subprocess.CalledProcessError as e:
                print(f"{colours.RED}Error{colours.END} copying a_over_q: {e}")

        # CREATE DATA LINK
        if source_folder_paths:
            source_folder_path = source_folder_paths[
                0
            ]  # Update the value inside the if block
            try:
                subprocess.run(
                    [
                        "ln",
                        "-s",
                        source_folder_path + data_folder_pattern,
                        destination_folder_path,
                    ],
                    check=True,
                )
                print(
                    f"Symbolic link created {colours.GREEN}successfully{colours.END} for folder: {source_folder_path+data_folder_pattern} to {destination_folder_path}"
                )
                data = True
            except subprocess.CalledProcessError as e:
                print(
                    f"{colours.RED}Error{colours.END} creating symbolic link for folder: {e}"
                )

        else:
            print(
                f"No matching source folder found for pattern: {source_folder_pattern}"
            )

        # CREATE PRISMA DATA LINK
        source_file_pattern = f"{source_folder_path+data_folder_pattern}/ancillaries/BU_ancillaries_i*_{run_number:04d}_*.adf"
        # destination_file_path = f"run_{run_number:04d}/prisma_0000.adf"

        source_file_paths = glob.glob(source_file_pattern)

        for source_file_path in source_file_paths:
            # TAKE SUFFIX NUMBER
            file_suffix = os.path.basename(source_file_path)[-8:-4]
            destination_file_path_with_suffix = (
                f"run_{run_number:04d}/prisma_{file_suffix}.adf"
            )

            try:
                subprocess.run(
                    ["ln", "-s", source_file_path, destination_file_path_with_suffix],
                    check=True,
                )
                print(
                    f"Symbolic link created {colours.GREEN}successfully{colours.END} for file: {destination_file_path_with_suffix}"
                )
                prismadata = True
            except subprocess.CalledProcessError as e:
                print(
                    f"{colours.RED}Error{colours.END} creating symbolic link for file: {e}"
                )

    # IF SETUP IS SKIPPED SET ALL TO TRUE
    else:
        folder = True
        conf = True
        genconf = True
        aoverq = True
        prismaconf = True
        data = True
        prismadata = True

    # IF SETUP WAS SUCCESSFUL RUN GENCONF AND FEMUL ON DATA
    if folder and conf and genconf and aoverq and prismaconf and data and prismadata:
        os.chdir(destination_folder_path)
        with open(log_path, "a") as file:
            file.write("Trying femul... ")
        if do_genconf:
            subprocess.run(["python2.7", "gen_conf.py"], check=True)
            if do_femul:
                subprocess.run(["femul", "Topology_FromPSAToTreePRISMA.conf"])
                with open(log_path, "a") as file:
                    file.write("SUCCESS, please check femul output\n")
        else:
            with open(log_path, "a") as file:
                file.write(f"FAILURE, {do_femul}\n")
        os.chdir(current_directory)
        print(f"\n{colours.GREEN}SUCCESS!!!!{colours.END}\n")

    else:
        print(
            f"\n{colours.RED}There was a problem with one of the parts{colours.END}\n"
        )
        with open(log_path, "a") as file:
            file.write(
                f"NO GENCONF: {folder} {conf}  {genconf}  {prismaconf} {data} {prismadata}\n"
            )

    current_datetime = datetime.now()
    with open(log_path, "a") as file:
        file.write(
            "End time:\t" + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <2-digit-number1> <2-digit-number2> ...")
        sys.exit(1)

    skip_runs = [14, 15, 18, 25, 35, 38]

    try:
        for arg in sys.argv[1:]:
            run_number = int(arg)
            if 16 <= run_number <= 50:
                if run_number not in skip_runs:
                    setup_femul(run_number)
                else:
                    print(f"Skipping run {run_number} as it is in the skip_runs list.")
            else:
                print(
                    f"Skipping invalid run {run_number}. It must be between 16 and 50."
                )
    except ValueError:
        print("Invalid input. Please provide valid 2-digit numbers.")
