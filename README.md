In terminal:

- wsl.exe --list --online
- wsl.exe --install Debian
- wsl

In WSL:

- sudo apt update && sudo apt upgrade
- sudo apt install python3-full python3-pip python3-venv smartmontools
- cd /mnt/c/Dev/vima.smart_emails
- python3 -m venv ./.wsl-venv
- source ./.wsl-venv/bin/activate
- make install