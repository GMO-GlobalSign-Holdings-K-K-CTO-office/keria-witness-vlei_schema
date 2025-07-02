import argparse
import os
import subprocess
import sys

CONFIG_DIR = "/usr/local/config"

def run_command(command):
    """
    Executes a command and displays its output in real-time.
    Exits with an error if the command fails.
    """
    print(f"Executing: {' '.join(command)}")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in process.stdout:
            sys.stdout.write(line)
        process.wait()
        if process.returncode != 0:
            print(f"Error: Command failed with exit code {process.returncode}", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found. Make sure '{command[0]}' is in your PATH.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A script to execute KLI commands (positional arguments version)")

    # Add positional arguments
    # 'required=True' is default for positional arguments
    parser.add_argument("witness_name", help="witness name (1st argument)")
    parser.add_argument("tcp_port", type=int, help="TCP Port Number (2nd argument)")
    parser.add_argument("http_port", type=int, help="HTTP Port Number (3rd argument)")

    args = parser.parse_args()

    # Dictionary holding keystore names and their corresponding Salt values
    # IMPORTANT: Do not hard-code sensitive information like salts in production code!!
    salt_dict = {
        "wit1": "0ABk5t3L527Hwx4hELaUobDl",
        "wit2": "0ACP-C_tQ8DW2cPIy_evhn3N",
        "wit3": "0AD2XHz4o5wxSgstSwEpqtQt",
        "wit4": "0ACBV3L_hMGhoOG3puG5qAA2",
        "wit5": "0ACeGTQVZZluNuXoRb7eRPwt"
    }

    # Retrieve the Salt value corresponding to the provided keystore name
    # If not found in the dictionary, a warning is printed and a default value is used.
    salt_value = salt_dict.get(args.witness_name)
    if salt_value == "default_salt_for_new_keystore":
        print(f"Warning: Salt value for '{args.witness_name}' not found in internal dictionary. Using default salt: '{salt_value}'.")
    else:
        print(f"Using Salt value '{salt_value}' for keystore '{args.witness_name}'.")

    # Execute the series of commands
    # 1. kli init
    init_cmd = ["kli", "init", "-n", args.witness_name, "-s", salt_value, "--nopasscode", "-c", CONFIG_DIR, "--config-file", args.witness_name]
    run_command(init_cmd)

    # 2. kli incept
    incept_cmd = ["kli", "incept", "-n", args.witness_name, "-a", args.witness_name, "-f", os.path.join(CONFIG_DIR, "incept.json")]
    run_command(incept_cmd)

    # 3. kli witness start
    witness_start_cmd = [
        "kli", "witness", "start",
        "-n", args.witness_name,
        "-a", args.witness_name,
        "-T", str(args.tcp_port),
        "-H", str(args.http_port),
        "-loglevel", "INFO"
    ]
    run_command(witness_start_cmd)

    print("\nAll KLI commands executed successfully!")

if __name__ == "__main__":
    main()