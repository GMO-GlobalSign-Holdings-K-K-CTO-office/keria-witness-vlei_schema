import argparse
import os
import subprocess
import sys

CONFIG_DIR = "/usr/local/config"
PREF_DIR = "/usr/local/preference"

def run_command(command):
    """
    Executes a command and displays its output in real-time.
    Returns a tuple of (success, return_code) instead of exiting on error.
    
    Args:
        command: List of command and its arguments
        
    Returns:
        tuple: (success: bool, return_code: int)
            - success: True if command succeeded, False otherwise
            - return_code: The exit code of the command (0 for success)
    """
    print(f"Executing: {' '.join(command)}")
    sys.stdout.flush()
    
    try:
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=0
        )
        
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            sys.stdout.flush()
            
        process.wait()
        
        if process.returncode != 0:
            sys.stderr.flush()
            return False, process.returncode
        
        return True, 0
        
    except FileNotFoundError:
        sys.stderr.flush()
        return False, 127
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.stderr.flush()
        return False, 1

def main():
    parser = argparse.ArgumentParser(description="A script to execute KLI commands (positional arguments version)")

    # Add positional arguments
    # 'required=True' is default for positional arguments
    parser.add_argument("witness_name", help="witness name (1st argument)")
    parser.add_argument("tcp_port", type=int, help="TCP Port Number (2nd argument)")
    parser.add_argument("http_port", type=int, help="HTTP Port Number (3rd argument)")
    parser.add_argument("salt", help="Salt value (4th argument, optional)", nargs='?', default=None)

    args = parser.parse_args()

    # Execute the series of commands
    # 1. kli init
    init_cmd = ["kli", "init", "-n", args.witness_name, "--nopasscode", "-c", CONFIG_DIR, "--config-file", args.witness_name]

    # Add the salt value if args.salt defined.
    if args.salt:
        init_cmd.extend(["-s", args.salt])

    suc, retcode = run_command(init_cmd)
    if not suc:
        print(f"Habery initialization failed with return code {retcode}. Exiting.", file=sys.stderr)
        sys.exit(retcode)

    # 2. kli incept
    incept_cmd = ["kli", "incept", "-n", args.witness_name, "-a", args.witness_name, "-c", CONFIG_DIR, "-f", os.path.join(PREF_DIR, "incept.json")]
    suc, retcode = run_command(incept_cmd)
    if not suc:
        if retcode == 255:
            print("Inception already completed. Skipping this step.")
        else:
            print(f"Inception failed with return code {retcode}. Exiting.", file=sys.stderr)
            sys.exit(retcode)

    # 3. kli witness start
    witness_start_cmd = [
        "kli", "witness", "start",
        "-n", args.witness_name,
        "-a", args.witness_name,
        "-T", str(args.tcp_port),
        "-H", str(args.http_port),
        "--loglevel", "INFO"
    ]
    suc, retcode = run_command(witness_start_cmd)
    if not suc:
        print(f"Witness start failed with return code {retcode}. Exiting.", file=sys.stderr)
        sys.exit(retcode)

    print("\nAll KLI commands executed successfully!")

if __name__ == "__main__":
    main()