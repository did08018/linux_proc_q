import paramiko

# Prompt the user for one or more IP addresses of Linux servers
ip_addresses = input("Enter the IP addresses of the Linux servers (comma-separated): ").split(",")

# Loop over the IP addresses and connect to each server
for ip_address in ip_addresses:
    print(f"Connecting to {ip_address}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username="your-username", password="your-password")

    # Prompt the user for a process name to query
    process_name = input(f"Enter the name of the process to query on {ip_address}: ")

    # Run the command to get the PID of the process
    stdin, stdout, stderr = ssh.exec_command(f"pgrep -d ' ' {process_name}")
    output = stdout.read().decode().strip()

    if output:
        pid = output.split()[0]
        print(f"Connected to {process_name} with PID {pid}")

        # Prompt the user for a query to run
        query = input(f"Enter a query to run on {process_name}: ")

        # Run the query on the process
        stdin, stdout, stderr = ssh.exec_command(f"sudo /bin/cat /proc/{pid}-pid/status | grep {query}")
        output = stdout.read().decode()

        print(f"Output of the query: {output}")
    else:
        print(f"Could not find process {process_name} on {ip_address}")

    # Close the SSH connection
    ssh.close()
