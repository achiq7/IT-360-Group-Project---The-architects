import csv
from datetime import datetime

#set the input file and destination file
INPUT_FILE = "ssh_logs.txt"
OUTPUT_FILE = "ssh_timeline.csv"

#read in the text file into a list
def readFile(filename: str) -> list[str]:
    data = []
    with open(filename, "r") as foFile:
        for line in foFile:
            line = line.strip()
            if line:
                data.append(line)
    return data

#organizes the elements in the list by the date provided
def organize_By_Date(log_File: list[str]) -> list[dict]:
    organizedLogs = []
    for line in log_File:
        parts = line.split(maxsplit=4)
        if len(parts) < 5:
            continue

        month, day, time_str, host, message = parts
        date_string = f"{month} {day} {time_str}"
#handles error exceptions
        try:
            dt = datetime.strptime(date_string, "%b %d %H:%M:%S")
            dt = dt.replace(year=datetime.now().year)
        except ValueError:
            continue

        organizedLogs.append({
            "datetime": dt,
            "date": dt.date().isoformat(),
            "time": dt.time().isoformat(timespec="seconds"),
            "host": host,
            "message": message
        })

    organizedLogs.sort(key=lambda e: e["datetime"])
    return organizedLogs

#produces timeline into csv file using the orgainzedLog list 
def write_timeline(organizedLogs: list[dict], output_file: str) -> None:
    fieldnames = ["datetime", "date", "time", "host", "message"]
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in organizedLogs:
            row = e.copy()
            row["datetime"] = e["datetime"].isoformat(sep=" ")
            writer.writerow(row)

#main function that calls functions
def main():
    log_File = readFile(INPUT_FILE)
    organizedLogs = organize_By_Date(log_File)
    write_timeline(organizedLogs, OUTPUT_FILE)
    print(f"Wrote {len(organizedLogs)} events to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
