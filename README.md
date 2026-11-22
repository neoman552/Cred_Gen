# MC2S Cred Gen

**MC2S Cred Gen** is a Python CLI tool that generates targeted `users.txt`, `passwords.txt`, and `login_password.txt` wordlists from organization metadata (`Company`, creation year, current/target year, locations, and special characters), including visual/leet mutations combined with special characters.

## Features

- Generates potential usernames (`users.txt`) based on common service/admin accounts, domain variations, years, and locations.
- Generates targeted password candidates (`passwords.txt`) using base words, years, common numbers, sequential patterns, and leet/visual substitutions (e.g., `Tun15i3@2o2G`).
- Combines usernames and passwords into `login:password` pairs (`login_password.txt`), with options to skip combination generation or omit comment headers.

## Usage

```bash
# Default run (reads info.txt in the current directory)
python3 cred_gen.py

# Specify input file and output directory
python3 cred_gen.py -i info.example.txt -o output/

# Generate only users.txt and passwords.txt without comment headers
python3 cred_gen.py -i info.txt --skip-combos --no-header
