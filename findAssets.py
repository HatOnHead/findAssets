import argparse
import subprocess
import os
import sys

def run_cmd(cmd):
    print(f"Running command: {cmd}")
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line.rstrip())
                lines.append(line.rstrip())
        return lines
    except Exception as e:
        print(f"Error running command {cmd}: {e}", file=sys.stderr)
        return []

def save_output(path, data):
    if not data:
        print("[!] No data to save.")
        return
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))
    print(f"Saved {len(data)} entries to {path}")

def subfinder(domain):
    print("[*] Running Subfinder...")
    res = run_cmd(f"subfinder -d {domain} -silent")
    print(f"[*] Subfinder found {len(res)} domains")
    return res

def amass(domain):
    print("[*] Running Amass passive enumeration...")
    res = run_cmd(f"amass enum -passive -d {domain}")
    print(f"[*] Amass found {len(res)} domains")
    return res

def httpx(input_list):
    print("[*] Running httpx to check live hosts...")
    temp_file = "temp_subs.txt"
    with open(temp_file, 'w') as f:
        f.write('\n'.join(input_list))
    res = run_cmd(f"httpx -l {temp_file} -silent -mc 200,302,403")
    print(f"[*] httpx found {len(res)} live domains")
    os.remove(temp_file)
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--subfinder', action='store_true')
    parser.add_argument('--amass', action='store_true')
    args = parser.parse_args()

    results = set()
    live_results = set()

    try:
        if args.subfinder:
            results.update(subfinder(args.domain))
        if args.amass:
            results.update(amass(args.domain))

        if not results:
            print("[!] No subdomains found, exiting.")
            sys.exit(1)

        live_results.update(httpx(list(results)))
        if not live_results:
            print("[!] No live domains found after httpx check, exiting.")
            sys.exit(1)

        save_output(args.output, sorted(live_results))
        print("[+] Finished asset collection.")

    except KeyboardInterrupt:
        print("\n[!] Detected interruption, saving collected results...")
        if live_results:
            save_output(args.output, sorted(live_results))
        elif results:
            print("[!] No live hosts checked yet, saving all collected subdomains.")
            save_output(args.output, sorted(results))
        else:
            print("[!] No data collected yet, nothing to save.")
        sys.exit(0)

if __name__ == "__main__":
    main()

