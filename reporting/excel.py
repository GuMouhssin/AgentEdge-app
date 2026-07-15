from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


def export_to_excel(businesses, filename="report.xlsx"):
    wb = Workbook()

    ws = wb.active
    ws.title = "Businesses"

    headers = [
        "Agency",
        "Lead Score",
        "rate",
        "Website",
        "Phone",
        "Emails",
        "Facebook",
        "Instagram",
        "LinkedIn",
        "YouTube",
        "Status",
    ]

    # Header style
    header_fill = PatternFill(
        start_color="1F4E78",
        end_color="1F4E78",
        fill_type="solid"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    hyperlink_font = Font(
        color="0563C1",
        underline="single"
    )

    green_fill = PatternFill(
        start_color="C6EFCE",
        end_color="C6EFCE",
        fill_type="solid"
    )

    yellow_fill = PatternFill(
        start_color="FFEB9C",
        end_color="FFEB9C",
        fill_type="solid"
    )

    red_fill = PatternFill(
        start_color="FFC7CE",
        end_color="FFC7CE",
        fill_type="solid"
    )

    # Headers
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font

    # Sort by lead score
    businesses.sort(
        key=lambda b: b.lead_score if b.lead_score is not None else -1,
        reverse=True
    )

    # Write businesses
    for row, business in enumerate(businesses, start=2):

        ws.cell(row=row, column=1).value = business.name

        # Lead score
        score_cell = ws.cell(row=row, column=2)
        score = business.lead_score or 0
        score_cell.value = score

        if score >= 80:
            score_cell.fill = green_fill
        elif score >= 50:
            score_cell.fill = yellow_fill
        else:
            score_cell.fill = red_fill

        #rate
        ws.cell(row=row, column=3).value = business.rate

        # Website
        website_cell = ws.cell(row=row, column=4)
        website_cell.value = business.website
        if business.website:
            website_cell.hyperlink = business.website
            website_cell.font = hyperlink_font

        # Phone
        ws.cell(row=row, column=5).value = business.phone

        # Emails
        ws.cell(row=row, column=6).value = "; ".join(business.emails)

        # Facebook
        fb_cell = ws.cell(row=row, column=7)
        fb_cell.value = business.facebook
        if business.facebook:
            fb_cell.hyperlink = business.facebook
            fb_cell.font = hyperlink_font

        # Instagram
        insta_cell = ws.cell(row=row, column=8)
        insta_cell.value = business.instagram
        if business.instagram:
            insta_cell.hyperlink = business.instagram
            insta_cell.font = hyperlink_font

        # LinkedIn
        li_cell = ws.cell(row=row, column=9)
        li_cell.value = business.linkedin
        if business.linkedin:
            li_cell.hyperlink = business.linkedin
            li_cell.font = hyperlink_font

        # YouTube
        yt_cell = ws.cell(row=row, column=10)
        yt_cell.value = business.youtube
        if business.youtube:
            yt_cell.hyperlink = business.youtube
            yt_cell.font = hyperlink_font

        # Status
        ws.cell(row=row, column=11).value = business.status

    # Auto-size columns
    for column in ws.columns:

        max_length = 0
        letter = get_column_letter(column[0].column)

        for cell in column:
            try:
                value = str(cell.value)
                if len(value) > max_length:
                    max_length = len(value)
            except Exception:
                pass

        ws.column_dimensions[letter].width = min(max_length + 3, 60)

    ws.freeze_panes = "A2"

    ws.auto_filter.ref = ws.dimensions

    wb.save(filename)