# SSH AutoConnect Logger
Pulls from list (hosts or ip's) to verify ssh login

Writes to the output file if the connection is successful (when result == "Success")

	Command-line arguments/usage:
    -u or --username: Specify the SSH username.
    -p or --password: Specify the SSH password.
    -l or --list: File containing the list of hosts (default is list.txt).
    -o or --output: File to log the SSH connection results (default is ssh_success_log.txt).
