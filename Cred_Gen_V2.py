#!/usr/bin/env python3
"""
MC2S Cred Gen v2.2
Generates username and password lists from company information,
including visual/leet mutations combined with special characters.
"""

import argparse
import datetime
import os
import sys


def display_banner():
    """
    Display ASCII banner for MC2S Cred Gen
    """
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ███╗ ██████╗██████╗ ███████╗     ██████╗██████╗ ███████╗██████╗     ║
║   ████╗ ████║██╔════╝╚════██╗██╔════╝    ██╔════╝██╔══██╗██╔════╝██╔══██╗    ║
║   ██╔████╔██║██║      █████╔╝███████╗    ██║     ██████╔╝█████╗  ██║  ██║    ║
║   ██║╚██╔╝██║██║     ██╔═══╝ ╚════██║    ██║     ██╔══██╗██╔══╝  ██║  ██║    ║
║   ██║ ╚═╝ ██║╚██████╗███████╗███████║    ╚██████╗██║  ██║███████╗██████╔╝    ║
║   ╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝     ║
║                                                                              ║
║                               MC2S Cred Gen                                  ║
║                    Generate: users.txt, passwords.txt, login_password.txt    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def read_info_file(filename):
    """
    Read information file and extract data
    """
    info = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="latin-1") as f:
            lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "Company":
                info["company"] = value
                clean_host = value.replace("www.", "")
                info["full_domain"] = clean_host
                info["company_domain"] = clean_host.split(".")[0] if "." in clean_host else clean_host
            elif key == "Year_of_creation":
                try:
                    info["year_of_creation"] = int(value)
                except ValueError:
                    info["year_of_creation"] = 2000
            elif key == "Actual_Year":
                if value.lower() == "current_year":
                    info["actual_year"] = datetime.datetime.now().year
                else:
                    try:
                        info["actual_year"] = int(value)
                    except ValueError:
                        info["actual_year"] = datetime.datetime.now().year
            elif key == "Location":
                locations = [loc.strip() for loc in value.split(",") if loc.strip()]
                if locations:
                    info["locations"] = locations
            elif key == "Char_Spec":
                special_chars = [char.strip() for char in value.split(",") if char.strip()]
                if special_chars:
                    info["special_chars"] = special_chars

    if "special_chars" not in info:
        info["special_chars"] = ["#", ".", "!", "$", "%", "_", "+", "-", ";", "@"]

    if "locations" not in info:
        info["locations"] = ["Default"]

    if "actual_year" not in info:
        info["actual_year"] = datetime.datetime.now().year

    if "year_of_creation" not in info:
        info["year_of_creation"] = 2000

    return info


def _build_company_name_without_tld(full_domain):
    if not full_domain:
        return ""
    parts = full_domain.split(".")
    if len(parts) > 1:
        return "".join(parts[:-1])
    return full_domain


def generate_usernames_from_info(info):
    """
    Generate username list based on company information
    """
    users = set()

    company = info.get("company_domain", "")
    full_domain = info.get("full_domain", "")
    company_name = _build_company_name_without_tld(full_domain)

    default_usernames = [
        "admin", "Admin", "ADMIN",
        "root", "Root", "ROOT",
        "administrator", "Administrator",
        "user", "User", "USER",
        "service", "Service", "SERVICE",
        "camera", "Camera", "CAMERA",
        "security", "Security", "SECURITY",
        "supervisor", "Supervisor", "SUPERVISOR",
        "operator", "Operator", "OPERATOR",
        "guest", "Guest", "GUEST",
        "tech", "Tech", "TECH",
        "support", "Support", "SUPPORT",
        "monitor", "Monitor", "MONITOR",
        "video", "Video", "VIDEO",
        "system", "System", "SYSTEM",
        "webmaster", "Webmaster", "WEBMASTER",
        "info", "Info", "INFO",
        "test", "Test", "TEST",
        "demo", "Demo", "DEMO",
        "backup", "Backup", "BACKUP",
        "ftp", "FTP", "ftpuser",
        "mysql", "Mysql", "MYSQL",
        "postgres", "Postgres", "POSTGRES",
        "oracle", "Oracle", "ORACLE",
        "www", "WWW", "www-data",
        "network", "Network", "NETWORK",
        "server", "Server", "SERVER",
        "client", "Client", "CLIENT",
        "manager", "Manager", "MANAGER",
        "staff", "Staff", "STAFF",
        "employee", "Employee", "EMPLOYEE",
        "helpdesk", "Helpdesk", "HELPDESK",
        "it", "IT", "itadmin",
    ]

    users.update(default_usernames)

    if company:
        raw_vars = [
            company,
            company.lower(),
            company.upper(),
            company.capitalize(),
            company_name,
            company_name.lower(),
            company_name.upper(),
            company_name.capitalize(),
        ]
        company_variations = []
        for v in raw_vars:
            if v and v not in company_variations:
                company_variations.append(v)

        for username in default_usernames[:20]:
            for company_var in company_variations[:4]:
                users.add(f"{username}_{company_var}")
                users.add(f"{username}.{company_var}")
                users.add(f"{username}-{company_var}")
                users.add(f"{company_var}_{username}")
                users.add(f"{company_var}.{username}")
                users.add(f"{company_var}-{username}")

        if full_domain:
            for username in ["admin", "administrator", "webmaster", "info", "support", "contact"]:
                users.add(f"{username}@{full_domain}")
                users.add(f"{username}_{full_domain.replace('.', '_')}")
                users.add(f"{username}_{full_domain.replace('.', '-')}")
                users.add(f"{full_domain.replace('.', '_')}_{username}")
                users.add(f"{full_domain.replace('.', '-')}_{username}")

        current_year = info.get("actual_year", datetime.datetime.now().year)
        creation_year = info.get("year_of_creation", 2000)

        for company_var in company_variations:
            users.add(company_var)
            users.add(f"{company_var}01")
            users.add(f"{company_var}001")
            users.add(f"{company_var}123")
            users.add(f"{company_var}{current_year}")
            users.add(f"{company_var}_admin")
            users.add(f"{company_var}_user")
            users.add(f"{company_var}_test")

        for username in default_usernames[:15]:
            users.add(f"{username}{current_year}")
            users.add(f"{username}{creation_year}")
            users.add(f"{username}_{current_year}")
            users.add(f"{username}_{creation_year}")

            for company_var in company_variations[:3]:
                users.add(f"{username}_{company_var}{current_year}")
                users.add(f"{company_var}_{username}{creation_year}")
                users.add(f"{username}{current_year}_{company_var}")

        locations = info.get("locations", [])
        for location in locations[:3]:
            location_clean = location.replace(" ", "").replace("-", "")
            if location_clean:
                users.add(f"admin_{location_clean}")
                users.add(f"{location_clean}_admin")
                users.add(f"user_{location_clean}")
                users.add(f"{location_clean}_user")

    return sorted(users)


def generate_visual_leet_passwords(info):
    """
    Generate visual/leet transformations on bases and years,
    combined with special characters from info.txt.
    Example pattern: Tun15i3@2o2G
    """
    results = set()

    company = info.get("company_domain", "")
    full_domain = info.get("full_domain", "")
    company_name = _build_company_name_without_tld(full_domain)
    creation_year = str(info.get("year_of_creation", 2000))
    current_year = str(info.get("actual_year", datetime.datetime.now().year))
    locations = info.get("locations", [])
    special_chars = info.get("special_chars", ["#", ".", "!", "$", "%", "_", "+", "-", ";", "@"])

    substitutions = {
        "a": ["@", "4"],
        "A": ["@", "4"],
        "e": ["3"],
        "E": ["3"],
        "i": ["1"],
        "I": ["1"],
        "l": ["1"],
        "L": ["1"],
        "o": ["0"],
        "O": ["0"],
        "s": ["5", "$"],
        "S": ["5", "$"],
        "t": ["7"],
        "T": ["7"],
        "b": ["8"],
        "B": ["8"],
        "g": ["9", "6"],
        "G": ["9", "6"],
        "z": ["2"],
        "Z": ["2"],
        # Visual digit-to-letter substitutions (e.g. 2026 -> 2o2G)
        "0": ["o", "O"],
        "1": ["l", "I"],
        "2": ["z"],
        "5": ["s", "S"],
        "6": ["G", "b"],
        "9": ["g"],
    }

    def mutate_token(token, max_variants=12):
        variants = {token}
        positions = [idx for idx, ch in enumerate(token) if ch in substitutions]

        # Single-character mutations
        for idx in positions:
            for repl in substitutions[token[idx]]:
                mutated = token[:idx] + repl + token[idx + 1 :]
                variants.add(mutated)
                if len(variants) >= max_variants:
                    return list(variants)

        # Pairwise mutations
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1, p2 = positions[i], positions[j]
                for r1 in substitutions[token[p1]]:
                    for r2 in substitutions[token[p2]]:
                        chars = list(token)
                        chars[p1] = r1
                        chars[p2] = r2
                        variants.add("".join(chars))
                        if len(variants) >= max_variants:
                            return list(variants)

        # Full substitution across all eligible positions
        full_chars = list(token)
        for idx in positions:
            full_chars[idx] = substitutions[token[idx]][0]
        variants.add("".join(full_chars))

        return list(variants)[:max_variants]

    raw_bases = []
    for item in [company, company_name] + locations:
        if item:
            clean = item.strip()
            raw_bases.extend([clean, clean.capitalize(), clean.lower(), clean.upper()])

    unique_bases = list(dict.fromkeys(b for b in raw_bases if len(b) >= 3))
    year_tokens = list(dict.fromkeys([current_year, creation_year, str(int(current_year) - 1)]))

    base_variants_map = {b: mutate_token(b, max_variants=10) for b in unique_bases}
    year_variants_map = {y: mutate_token(y, max_variants=8) for y in year_tokens}

    for base, b_vars in base_variants_map.items():
        for yr, y_vars in year_variants_map.items():
            for b_var in b_vars[:6]:
                for y_var in y_vars[:5]:
                    for sp in special_chars:
                        candidates = [
                            f"{b_var}{sp}{y_var}",
                            f"{y_var}{sp}{b_var}",
                            f"{b_var}{y_var}{sp}",
                            f"{sp}{b_var}{y_var}",
                        ]
                        for cand in candidates:
                            if len(cand) >= 6:
                                results.add(cand)

                    for sp in special_chars[:4]:
                        for cand in (f"{b_var}{y_var}{sp}", f"{sp}{b_var}{y_var}"):
                            if len(cand) >= 6:
                                results.add(cand)

    return results


def generate_passwords_from_info(info):
    """
    Generate passwords based on provided information
    """
    passwords = set()

    company = info.get("company_domain", "")
    full_domain = info.get("full_domain", "")
    company_name = _build_company_name_without_tld(full_domain)
    creation_year = info.get("year_of_creation", 2000)
    current_year = info.get("actual_year", datetime.datetime.now().year)
    locations = info.get("locations", [])
    special_chars = info.get("special_chars", ["#", ".", "!", "$", "%", "_", "+", "-", ";", "@"])

    years = list(
        dict.fromkeys(
            [
                creation_year,
                current_year,
                current_year - 1,
                current_year - 2,
                2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027,
                1970, 1980, 1990, 2000,
            ]
        )
    )

    common_numbers = [
        "123", "1234", "12345", "123456", "1234567", "12345678",
        "000", "0000", "00000", "000000", "0000000", "00000000",
        "111", "1111", "11111", "111111", "1111111", "11111111",
        "777", "7777", "77777", "777777",
        "888", "8888", "88888", "888888",
        "999", "9999", "99999", "999999",
        "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027",
        "007", "007007", "123123", "654321", "112233", "445566",
        "password", "Password", "PASSWORD",
        "admin", "Admin", "ADMIN", "netadmin", "administrator", "administrateur", "superadmin",
    ]

    bases = set()

    if company:
        bases.update([company, company.lower(), company.upper(), company.capitalize()])

    if company_name and company_name != company:
        bases.update([company_name, company_name.lower(), company_name.upper(), company_name.capitalize()])

    for location in locations:
        if location:
            bases.update([location, location.lower(), location.upper(), location.capitalize()])

    security_terms = [
        "admin", "Admin", "ADMIN",
        "security", "Security", "SECURITY",
        "pass", "Pass", "PASS",
        "password", "Password", "PASSWORD",
        "system", "System", "SYSTEM",
        "access", "Access", "ACCESS",
        "secure", "Secure", "SECURE",
        "user", "User", "USER",
        "login", "Login", "LOGIN",
        "server", "Server", "SERVER",
        "welcome", "Welcome", "WELCOME",
        "letmein", "Letmein", "LETMEIN",
        "master", "Master", "MASTER",
        "super", "Super", "SUPER",
        "company", "Company", "COMPANY",
        "business", "Business", "BUSINESS",
        "office", "Office", "OFFICE",
        "work", "Work", "WORK",
    ]
    bases.update(security_terms)

    bases_list = [b for b in bases if b]

    # 1. Base + Year
    for base in bases_list:
        for year in years:
            for candidate in (f"{base}{year}", f"{year}{base}"):
                if len(candidate) >= 4:
                    passwords.add(candidate)

            for special in special_chars[:4]:
                candidates = [
                    f"{base}{special}{year}",
                    f"{year}{special}{base}",
                    f"{base}{year}{special}",
                    f"{special}{base}{year}",
                ]
                for candidate in candidates:
                    if len(candidate) >= 6:
                        passwords.add(candidate)

                wrapped = f"{base}{special}{year}{special}"
                if len(wrapped) >= 8:
                    passwords.add(wrapped)

    # 2. Base + Common numbers
    for base in bases_list:
        for numbers in common_numbers:
            for candidate in (f"{base}{numbers}", f"{numbers}{base}"):
                if len(candidate) >= 6:
                    passwords.add(candidate)

            for special in special_chars[:3]:
                for candidate in (f"{base}{special}{numbers}", f"{numbers}{special}{base}"):
                    if len(candidate) >= 7:
                        passwords.add(candidate)

    # 3. Base combinations
    for i, base1 in enumerate(bases_list[:6]):
        for base2 in bases_list[i + 1 : min(i + 5, len(bases_list))]:
            for candidate in (f"{base1}{base2}", f"{base2}{base1}"):
                if len(candidate) >= 6:
                    passwords.add(candidate)

            for year in [creation_year, current_year]:
                candidate = f"{base1}{year}{base2}"
                if len(candidate) >= 8:
                    passwords.add(candidate)

            for special in special_chars[:3]:
                candidate = f"{base1}{special}{base2}"
                if len(candidate) >= 7:
                    passwords.add(candidate)

    # 4. Leet Speak variations
    leet_map = {
        "a": "@", "A": "@",
        "e": "3", "E": "3",
        "i": "1", "I": "1",
        "o": "0", "O": "0",
        "s": "$", "S": "$",
        "t": "7", "T": "7",
        "b": "8", "B": "8",
        "g": "9", "G": "9",
    }

    for base in bases_list:
        if len(base) >= 3:
            leet_base = "".join(leet_map.get(ch, ch) for ch in base)
            if leet_base != base:
                if len(leet_base) >= 4:
                    passwords.add(leet_base)

                for year in years[:4]:
                    for candidate in (f"{leet_base}{year}", f"{year}{leet_base}"):
                        if len(candidate) >= 6:
                            passwords.add(candidate)

                    for special in special_chars[:2]:
                        candidate = f"{leet_base}{special}{year}"
                        if len(candidate) >= 7:
                            passwords.add(candidate)

    # 5. Common passwords
    common_passwords = [
        "Password123", "Admin1234", "Secure2024", "System2024",
        "Welcome123", "Login2024", "Server2024", "Access2024",
        "Security2024", "Pass12345", "User2024", "Admin2024",
        "Secure2026", "Admin2026", "Welcome2026", "Password2026",
        "12345678", "123456789", "qwerty123", "password1",
        "admin123", "welcome1", "monkey123", "dragon123",
        "sunshine1", "master123", "hello123", "football123",
        "iloveyou1", "adminadmin", "superman123", "trustno1",
        "letmein123", "password123", "abc123",
        "password!", "admin!@#", "P@ssw0rd", "P@ssw0rd123",
        "Summer2026!", "Winter2026!", "Spring2026!", "Autumn2026!",
        "Company123!", "Business2026!", "Office123!",
    ]
    for pwd in common_passwords:
        if len(pwd) >= 6:
            passwords.add(pwd)

    # 6. Location-company-year patterns
    if locations and company:
        for location in locations[:3]:
            location_clean = location.replace(" ", "")
            if not location_clean:
                continue
            for year in [creation_year, current_year]:
                for special in special_chars[:3]:
                    patterns = [
                        f"{location_clean}{special}{company}{special}{year}",
                        f"{company}{special}{location_clean}{special}{year}",
                        f"{year}{special}{company}{special}{location_clean}",
                    ]
                    for pwd in patterns:
                        if len(pwd) >= 8:
                            passwords.add(pwd)

    # 7. Simple passwords
    simple_passwords = [
        f"{current_year}",
        f"{creation_year}",
        f"admin{current_year}",
        f"admin{creation_year}",
        f"password{current_year}",
        f"password{creation_year}",
        "admin", "password", "123456", "qwerty", "letmein", "welcome",
        "pass", "Pass", "PASS", "Admin", "ADMIN",
    ]
    if company:
        simple_passwords.extend(
            [
                company,
                company.lower(),
                company.upper(),
                f"{company}123",
                f"{company}!",
                f"{company}@123",
                f"{company}#123",
            ]
        )

    for pwd in simple_passwords:
        if pwd and len(pwd) >= 4:
            passwords.add(pwd)

    # 8. Sequential patterns
    sequential_patterns = [
        "123456", "12345678", "123456789", "1234567890",
        "abcdef", "abcdefgh", "qwerty", "qwertyuiop",
        "asdfgh", "asdfghjkl", "zxcvbn", "zxcvbnm",
        "111111", "222222", "333333", "444444",
        "555555", "666666", "777777", "888888",
        "999999", "000000", "121212", "131313",
    ]
    for pattern in sequential_patterns:
        if len(pattern) >= 6:
            passwords.add(pattern)

    # 9. Visual / Leet mutations combined with special characters
    passwords.update(generate_visual_leet_passwords(info))

    return sorted(passwords, key=lambda x: (len(x), x))


def save_login_password_file(users, passwords, output_filename="login_password.txt", include_header=True):
    total_combinations = len(users) * len(passwords)

    with open(output_filename, "w", encoding="utf-8") as f:
        if include_header:
            f.write("# Login:Password combinations file\n")
            f.write("# Format: login:password\n")
            f.write(f"# Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Number of usernames: {len(users)}\n")
            f.write(f"# Number of passwords: {len(passwords)}\n")
            f.write(f"# Total combinations: {total_combinations}\n")
            f.write("#" * 70 + "\n\n")

        for user in users:
            for password in passwords:
                f.write(f"{user}:{password}\n")

    return total_combinations


def save_users_file(users, output_filename="users.txt", include_header=True):
    with open(output_filename, "w", encoding="utf-8") as f:
        if include_header:
            f.write("# Generated username list\n")
            f.write(f"# Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Number of usernames: {len(users)}\n")
            f.write("#" * 50 + "\n\n")

        for user in users:
            f.write(f"{user}\n")

    return len(users)


def save_passwords_file(passwords, output_filename="passwords.txt", include_header=True):
    with open(output_filename, "w", encoding="utf-8") as f:
        if include_header:
            f.write("# Generated password list\n")
            f.write(f"# Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Number of passwords: {len(passwords)}\n")
            f.write("#" * 50 + "\n\n")

        for password in passwords:
            f.write(f"{password}\n")

    return len(passwords)


def parse_args():
    parser = argparse.ArgumentParser(description="MC2S Cred Gen - Generate usernames, passwords, and login:password wordlists.")
    parser.add_argument("-i", "--input", default="info.txt", help="Input info file (default: info.txt)")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--no-header", action="store_true", help="Omit comment headers from generated files")
    parser.add_argument("--skip-combos", action="store_true", help="Do not generate login_password.txt")
    return parser.parse_args()


def main():
    args = parse_args()
    display_banner()

    print("\n" + "=" * 70)
    print("MC2S CRED GEN - CREDENTIAL WORDLIST GENERATOR")
    print("=" * 70)

    info_filename = args.input
    try:
        info = read_info_file(info_filename)
        print(f"\n[✓] File '{info_filename}' read successfully")
        print(f"   • Company: {info.get('company', 'Not specified')}")
        print(f"   • Full domain: {info.get('full_domain', 'N/A')}")
        print(f"   • Year of creation: {info.get('year_of_creation', 'Not specified')}")
        print(f"   • Current year: {info.get('actual_year', 'Not specified')}")
        print(f"   • Locations: {', '.join(info.get('locations', []))}")
        print(f"   • Special characters: {', '.join(info.get('special_chars', []))}")
    except FileNotFoundError:
        print(f"\n[✗] File '{info_filename}' not found")
        print("Creating example info.txt file...")

        example_content = """# Separation is ,
Company:Test.com
Year_of_creation:2000
Actual_Year:Current_year
Location:Tunisie, Tunis
Char_Spec:#,.,!,$,%,_,+,-,;,@"""

        with open(info_filename, "w", encoding="utf-8") as f:
            f.write(example_content)

        print(f"[✓] Example created in '{info_filename}'")
        print("Please modify this file with your information and run the script again.")
        return
    except Exception as e:
        print(f"\n[✗] Error reading file: {e}")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    include_header = not args.no_header

    users = generate_usernames_from_info(info)
    passwords = generate_passwords_from_info(info)

    users_path = os.path.join(args.output_dir, "users.txt")
    passwords_path = os.path.join(args.output_dir, "passwords.txt")
    combos_path = os.path.join(args.output_dir, "login_password.txt")

    users_count = save_users_file(users, users_path, include_header=include_header)
    passwords_count = save_passwords_file(passwords, passwords_path, include_header=include_header)

    if not args.skip_combos:
        combinations_count = save_login_password_file(users, passwords, combos_path, include_header=include_header)
    else:
        combinations_count = 0

    print("\n" + "-" * 70)
    print("STATISTICAL SUMMARY")
    print("-" * 70)
    print(f"• Usernames generated: {users_count}")
    print(f"• Passwords generated: {passwords_count}")
    if not args.skip_combos:
        print(f"• Total combinations: {combinations_count:,}")

    print("\n" + "=" * 70)
    print("⚠️  RESPONSIBLE USE REQUIRED")
    print("=" * 70)
    print("Use ONLY for authorized audits, labs, and training exercises.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[✗] Unexpected error: {e}")
        sys.exit(1)