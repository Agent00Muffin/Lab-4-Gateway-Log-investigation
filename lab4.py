from log_analysis import get_log_file_path_from_cmd_line, filter_log_by_regex
import pandas as pd
import re

def main():
    ip_address = "220.195.35.40"
    log_file = get_log_file_path_from_cmd_line(1)
    port_traffic = tally_port_traffic(log_file)
    generate_invalid_user_report(log_file)
    generate_source_ip_log(log_file, ip_address)

    for port_num, count in port_traffic.items():
        if count >= 100:
            generate_port_traffic_report(log_file, port_num)

    pass

def tally_port_traffic(log_file):
    data = filter_log_by_regex(log_file, r'DPT=(.+?) ')[1]
    port_traffic = {}
    for d in data:
        port = d[0]
        port_traffic[port] = port_traffic.get(port, 0) + 1
    return port_traffic

def generate_port_traffic_report(log_file, port_number):

    regex = r'(.{6}) (.{8}) .*SRC=(.+) DST=(.+?) .+SPT=(.+) ' + f'DPT=({port_number})'
    data= filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(data)
    header_row = ("Date", 'Time', 'Source IP Address', 'Destination IP Address', 'Source Port', 'Destination port')
    report_df.to_csv(f'destination_port_{port_number}_report.csv', index=False, header=header_row)
    return

def generate_invalid_user_report(log_file):

    regex = r'(.{3} \d{2}) (\d{2}:\d{2}:\d{2}) myth sshd\[\d{5}]: Invalid user (\D+) from (\d{3}\.\d{3}\.\d{2}\.\d{2})'
    data= filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(data)
    header_row =  ("Date", "Time", "Username", "IP Address")
    report_df.to_csv(f'invalid_users.csv', index=False, header=header_row)
    return

def generate_source_ip_log(log_file, ip_address):

    regex = r'(.+?) ' + f'SRC=({ip_address})' + r'(.+)'
    data= filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(data)
    clean_ip = re.sub(r'\.', '_', f'{ip_address}')
    report_df.to_csv(f'source_ip_{clean_ip}.log', index=False)
    return

if __name__ == '__main__':
    main()