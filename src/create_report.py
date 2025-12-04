import csv
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

#takes in csv and sets destination pdf file 
TIMELINE_FILE = "ssh_timeline.csv"
REPORT_FILE = "Forensic_Timeline_Report.pdf"

#reads in the event from the csv file
def load_events(csv_path):
    events = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # parse datetime string to datetime object for ordering
            dt = datetime.fromisoformat(row["datetime"])
            row["dt_obj"] = dt
            events.append(row)

    # sorts just in case
    events.sort(key=lambda e: e["dt_obj"])
    return events

#formats the actual pdf
def build_report(events, output_pdf):
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # customizes smaller text for table
    table_style = ParagraphStyle(
        "TableText",
        parent=normal_style,
        fontSize=8,
        leading=10,
    )
	#formats the layout of the page
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=LETTER,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40,
    )

    story = []

    # Title
    story.append(Paragraph("Digital Forensic Timeline Report", title_style))
    story.append(Spacer(1, 12))

    # Overview
    num_events = len(events)
    if num_events > 0:
        first_event = events[0]["datetime"]
        last_event = events[-1]["datetime"]
    else:
        first_event = last_event = "N/A"

    overview_text = f"""
    This report summarizes the SSH-related system activity captured and processed
    by the Digital Forensic Timeline Builder. The source data originates from
    SSH log entries on the Kali Linux system and has been forwarded into a
    chronological event timeline.

    <br/><br/>
    <b>Total events:</b> {num_events}<br/>
    <b>First event:</b> {first_event}<br/>
    <b>Last event:</b> {last_event}<br/>
    """
    story.append(Paragraph(overview_text, normal_style))
    story.append(Spacer(1, 12))

    # Methodology 
    story.append(Paragraph("Methodology", heading_style))
    methodology_text = """
    Log entries were collected from the SSH logging source on the Kali Linux
    virtual machine and written to a text file. Each line was parsed to extract
    the timestamp, host, and message fields. Timestamps were converted to a
    consistent datetime format and sorted chronologically. The resulting
    normalized records were stored in a CSV file (<i>ssh_timeline.csv</i>).
    """
    story.append(Paragraph(methodology_text, normal_style))
    story.append(Spacer(1, 12))

    # Sample Timeline Table
    story.append(Paragraph("Sample Timeline Entries", heading_style))

    # table header
    table_data = [["Datetime", "Host", "Message"]]

    # include first N events (keeps PDF readable)
    max_rows = 25
    for event in events[:max_rows]:
        table_data.append(
            [
                event["datetime"],
                event.get("host", ""),
                event.get("message", "")[:80],  # truncate long messages
            ]
        )
	#styling
    table = Table(table_data, colWidths=[130, 60, 320])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 7),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 12))

    # Findings/Observations
    story.append(Paragraph("Findings and Observations", heading_style))
    findings_text = """
    The timeline shows the sequence of SSH-related events in the system,
    including authentication attempts and general SSH activity. By
    reviewing the timestamps and messages, an analyst can identify patterns
    such as repeated failed login attempts, unusual login times, or suspicious
    activity that may call for further investigation.
    """
    story.append(Paragraph(findings_text, normal_style))

    # build the PDF
    doc.build(story)

#calls other functions
def main():
    events = load_events(TIMELINE_FILE)
    build_report(events, REPORT_FILE)
    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
