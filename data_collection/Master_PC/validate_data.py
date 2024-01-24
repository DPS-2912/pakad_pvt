import subprocess
import paramiko

def run_command(command):
    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # An error occurred while executing the command
        print("Command execution failed with error:")
        print(e.stderr)

def scp_file(source_path, destination_path, hostname, username, password):
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        client.connect(hostname=hostname, username=username, password=password)

        # Create an SCP client
        scp = client.open_sftp()

        # Transfer the file from the remote server to the local machine
        scp.get(source_path, destination_path)

        # Close the SCP connection
        scp.close()

        print("File transferred successfully!")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        # Close the SSH connection
        client.close()


def check_if_valid():
    scp_file('/home/ubuntu/shared_folder/list_of_errors.txt', './satlink_list_of_errors.txt', '192.168.1.99', 'ubuntu', 'ubuntu')
    scp_file('/home/ubuntu/shared_folder/list_of_errors.txt', './fiber_list_of_errors.txt', '129.97.84.27', 'ubuntu', 'ubuntu')


    run_command("grep '_.*_' satlink_list_of_errors.txt > satlink_webpages_all.txt")
    run_command("sed 's/..$//' satlink_webpages_all.txt > satlink_webpages_new.txt")
    run_command("sort satlink_webpages_new.txt | uniq -c | awk '$1 == 7 {print $2}' > satlink_webpages_errors.txt")
    run_command("sed 's/_.*//' satlink_webpages_errors.txt > satlink_webpages_all.txt")
    run_command("sort satlink_webpages_all.txt | uniq -c > satlink_errors_final.txt")
    run_command("rm satlink_webpages*")

    run_command("grep '_.*_' fiber_list_of_errors.txt > satlink_webpages_all.txt")
    run_command("sed 's/..$//' satlink_webpages_all.txt > satlink_webpages_new.txt")
    run_command("sort satlink_webpages_new.txt | uniq -c | awk '$1 == 7 {print $2}' > satlink_webpages_errors.txt")
    run_command("sed 's/_.*//' satlink_webpages_errors.txt > satlink_webpages_all.txt")
    run_command("sort satlink_webpages_all.txt | uniq -c > fiber_errors_final.txt")
    run_command("rm satlink_webpages*")

    filename = './fiber_errors_final.txt'
    second_words = []
    count = 0

    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            if len(words) > 0:
                first_word = words[0]
                second_word = words[1]
                if int(first_word) > 7:
                    count = count + 1
                    second_words.append(second_word)

    filename = './satlink_errors_final.txt'

    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            if len(words) > 0:
                first_word = words[0]
                second_word = words[1]
                if int(first_word) > 7 and second_word not in second_words:
                    count = count + 1

    return count
