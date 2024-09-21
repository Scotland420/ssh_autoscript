import paramiko
import argparse
import time
import socket

# Function to attempt SSH connection
def ssh_to_host(hostname, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        
        # Automatically add host keys from the remote machines
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the host
        client.connect(hostname, username=username, password=password, timeout=10)
        
        # If the connection was successful
        return "Success"
    
    except paramiko.AuthenticationException:
        # If there is an authentication error (wrong username/password)
        return "Failed: Authentication Error (Wrong username/password)"
    
    except socket.timeout:
        # If there is a connection timeout
        return "Failed: Connection Timeout to host"
    
    except paramiko.SSHException as e:
        # If there is any other SSH-related issue
        return f"Failed: SSH Error ({str(e)})"
    
    except Exception as e:
        # Handle any other general exceptions
        return f"Failed: {str(e)}"
    
    finally:
        # Close the connection if it's open
        client.close()

# Function to handle SSH attempts
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="SSH into multiple machines and log successes")
    parser.add_argument('-u', '--username', required=True, help="SSH username")
    parser.add_argument('-p', '--password', required=True, help="SSH password")
    parser.add_argument('-l', '--list', default='list.txt', help="File containing list of hosts")
    parser.add_argument('-o', '--output', default='ssh_success_log.txt', help="File to write success logs")
    
    args = parser.parse_args()

    # Read list of IPs or hostnames from the specified file
    with open(args.list, 'r') as file:
        hosts = file.readlines()

    # Remove newline characters
    hosts = [host.strip() for host in hosts]

    # Open the log file in append mode
    with open(args.output, 'a') as log:
        for host in hosts:
            # Attempt SSH connection
            result = ssh_to_host(host, args.username, args.password)
            
            # Print the result to the terminal
            print(f"{result}: {host}")
            
            # Only write successful connections to the log file
            if result == "Success":
                log.write(f"Success: SSH to {host} was successful.\n")
            
            # Sleep between connections to avoid rapid retries
            time.sleep(1)

if __name__ == "__main__":
    main()
