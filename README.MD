A simple interactive Python tool that automates local port forwarding using Bore and generates ready-to-use reverse shell payloads from a JSON database.

Features:
Dynamic Port Mapping: Automatically starts bore and extracts the remote public port using Regex.
Interactive Menu: Choose from multiple pre-configured payloads like Bash, Python, PHP, and PowerShell.
TTY Stability: Includes optimized smart payloads to provide interactive shells with Tab-completion and history support.

Structure:
main.py: The main script that runs the tunnel and the menu.
rs.json: Database containing all the reverse shell templates.
README.md: Project documentation.


use: sudo apt install bore -y
termux: pkg install bore -y

Start your local listener in a separate terminal: nc -lvnp 4444

python3 main.py 

Enter your local port, choose a payload from the menu, and execute the generated command on the target machine.

