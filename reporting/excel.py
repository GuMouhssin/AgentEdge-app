from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side
)
from openpyxl.utils import get_column_letter
from datetime import datetime


def safe(value):
    if value is None or (isinstance(value, float) and str(value) == "nan"):
        return "N/A"
    return value


def add_summary_sheet(wb, businesses, city):
    ws = wb.create_sheet("Summary", 0)

    total        = len(businesses)
    hot          = sum(1 for b in businesses if (b.lead_score or 0) >= 80)
    warm         = sum(1 for b in businesses if 50 <= (b.lead_score or 0) < 80)
    cold         = sum(1 for b in businesses if (b.lead_score or 0) < 50)
    with_email   = sum(1 for b in businesses if b.emails)
    with_phone   = sum(1 for b in businesses if b.phone)
    with_website = sum(1 for b in businesses if b.website)
    with_social  = sum(1 for b in businesses if any([
                       b.facebook, b.instagram,
                       b.linkedin, b.youtube]))

    valid_ratings = [
        float(b.rate) for b in businesses
        if b.rate and safe(b.rate) != "N/A"
    ]
    avg_rating = (
        sum(valid_ratings) / len(valid_ratings)
        if valid_ratings else 0
    )

    # ── Styles ──────────────────────────────────────────
    title_font    = Font(bold=True, size=16, color="1F4E78", name="Calibri")
    subtitle_font = Font(size=10, color="6B7280", italic=True, name="Calibri")
    label_font    = Font(size=10, color="374151", name="Calibri")
    value_font    = Font(bold=True, size=10, color="1F4E78", name="Calibri")
    note_font     = Font(size=9, color="6B7280", italic=True, name="Calibri")

    navy_fill   = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    green_fill  = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    red_fill    = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    sky_fill    = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

    thin   = Side(style="thin", color="E5E7EB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    center = Alignment(horizontal="center", vertical="center")
    left   = Alignment(horizontal="left",   vertical="center")

    # ── Title block ──────────────────────────────────────
    ws.merge_cells("A1:D1")
    t           = ws["A1"]
    t.value     = "AgentEdge — Competitor Intelligence Report"
    t.font      = title_font
    t.fill      = sky_fill
    t.alignment = left
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:D2")
    s           = ws["A2"]
    s.value     = (
        f"City: {city}  |  "
        f"Generated: {datetime.now().strftime('%d %B %Y')}  |  "
        f"Powered by AgentEdge"
    )
    s.font      = subtitle_font
    s.fill      = sky_fill
    s.alignment = left
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 10  # spacer

    # ── Section header ───────────────────────────────────
    ws.merge_cells("A4:D4")
    h           = ws["A4"]
    h.value     = "REPORT SUMMARY"
    h.font      = Font(bold=True, size=11, color="FFFFFF", name="Calibri")
    h.fill      = navy_fill
    h.alignment = center
    ws.row_dimensions[4].height = 22

    # ── Stats ────────────────────────────────────────────
    stats = [
        ("Total Agencies Found",           total,                      None),
        ("🟢 Hot Leads (score 80+)",        hot,                        green_fill),
        ("🟡 Warm Leads (score 50-79)",     warm,                       yellow_fill),
        ("🔴 Cold Leads (score below 50)",  cold,                       red_fill),
        (None, None, None),
        ("Agencies with Email",            f"{with_email} / {total}",   None),
        ("Agencies with Phone",            f"{with_phone} / {total}",   None),
        ("Agencies with Website",          f"{with_website} / {total}", None),
        ("Agencies with Social Media",     f"{with_social} / {total}",  None),
        (None, None, None),
        ("Average Google Rating",          f"{avg_rating:.1f} / 5.0",   None),
    ]

    for i, (label, value, fill) in enumerate(stats, start=5):
        if label is None:
            ws.row_dimensions[i].height = 8
            continue

        label_cell           = ws.cell(row=i, column=1)
        label_cell.value     = label
        label_cell.font      = label_font
        label_cell.alignment = left
        label_cell.border    = border

        value_cell           = ws.cell(row=i, column=2)
        value_cell.value     = value
        value_cell.font      = value_font
        value_cell.alignment = center
        value_cell.border    = border

        if fill:
            label_cell.fill = fill
            value_cell.fill = fill

        ws.row_dimensions[i].height = 20

    # ── Note ─────────────────────────────────────────────
    last_row = 5 + len(stats) + 2
    ws.merge_cells(f"A{last_row}:D{last_row}")
    note           = ws.cell(row=last_row, column=1)
    note.value     = "-> See the 'Agencies' sheet for full competitor details with contact info and social profiles."
    note.font      = note_font
    note.alignment = left

    # ── Column widths ────────────────────────────────────
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 18


def export_to_excel(businesses, filename="report.xlsx",
                    limit=None, city="Unknown City"):

    wb = Workbook()

    # Grab the original default sheet BEFORE creating the Summary sheet.
    # (create_sheet("Summary", 0) inserts at index 0 and pushes the default
    # sheet to index 1, but wb.active is still index 0 — so if we asked for
    # wb.active *after* creating Summary, we'd get the Summary sheet back
    # by mistake and end up renaming/overwriting it instead of using the
    # blank sheet. Grabbing the reference now avoids that.)
    ws = wb.active

    # ── Summary sheet ────────────────────────────────────
    add_summary_sheet(wb, businesses, city)

    # ── Agencies sheet ───────────────────────────────────
    ws.title = "Agencies"

    headers = [
        "Agency",
        "Lead Score",
        "Rating",
        "Reviews",
        "Website",
        "Phone",
        "Emails",
        "Google Maps",
        "Facebook",
        "Instagram",
        "LinkedIn",
        "YouTube",
    ]

    # ── Styles ───────────────────────────────────────────
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=10, name="Calibri")
    green_fill  = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    red_fill    = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    sky_fill    = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
    alt_fill    = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    thin   = Side(style="thin", color="E5E7EB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    center = Alignment(horizontal="center", vertical="center")
    left   = Alignment(horizontal="left",   vertical="center")

    # ── Row 1: Title ─────────────────────────────────────
    title_col = get_column_letter(len(headers))

    ws.merge_cells(f"A1:{title_col}1")

    title_cell = ws["A1"]
    title_cell.value = (
        f"AgentEdge — {city} Competitor Intelligence Report  |  "
        f"Generated: {datetime.now().strftime('%d %B %Y')}"
    )

    title_cell.font = Font(
        bold=True,
        size=12,
        color="1F4E78",
        name="Calibri"
    )

    title_cell.fill = sky_fill
    title_cell.alignment = left

    ws.row_dimensions[1].height = 26

    # ── Row 2: Headers ───────────────────────────────────
    for col, header in enumerate(headers, start=1):
        c           = ws.cell(row=2, column=col)
        c.value     = header
        c.fill      = header_fill
        c.font      = header_font
        c.alignment = center
        c.border    = border
    ws.row_dimensions[2].height = 22

    # ── Sort & limit ─────────────────────────────────────
    businesses.sort(
        key=lambda b: b.lead_score if b.lead_score is not None else -1,
        reverse=True
    )
    export_list = businesses[:limit] if limit else businesses

    # ── Write data rows ───────────────────────────────────
    for row_idx, business in enumerate(export_list, start=3):

        use_alt = (row_idx % 2 == 0)

        def write_cell(col, value, hyperlink=None, bold=False,
                       align=left, custom_fill=None):
            c           = ws.cell(row=row_idx, column=col)
            c.value     = value
            c.font      = Font(
                color     = "0563C1" if hyperlink else "111827",
                underline = "single" if hyperlink else None,
                size      = 9,
                bold      = bold,
                name      = "Calibri"
            )
            c.alignment = align
            c.border    = border
            if hyperlink:
                c.hyperlink = hyperlink
            if custom_fill:
                c.fill = custom_fill
            elif use_alt:
                c.fill = alt_fill

        # Col 1 — Agency name
        write_cell(1, safe(business.name), bold=True)

        # Col 2 — Lead score (colored)
        score      = business.lead_score if business.lead_score is not None else 0
        score_fill = (
            green_fill  if score >= 80 else
            yellow_fill if score >= 50 else
            red_fill
        )
        sc           = ws.cell(row=row_idx, column=2)
        sc.value     = score
        sc.font      = Font(bold=True, size=9, name="Calibri")
        sc.fill      = score_fill
        sc.alignment = center
        sc.border    = border

        # Col 3 — Rating (X / 5)
        rating     = safe(business.rate)
        rating_str = f"{rating} / 5" if rating != "N/A" else "N/A"
        write_cell(3, rating_str, align=center)

        # Col 4 — Reviews
        write_cell(4, safe(business.reviews), align=center)

        # Col 5 — Website
        website = safe(business.website)
        write_cell(
            5, website,
            hyperlink=website if website != "N/A" else None
        )

        # Col 6 — Phone
        write_cell(6, safe(business.phone))

        # Col 7 — Emails
        emails_val = (
            "; ".join(business.emails)
            if business.emails else "N/A"
        )
        write_cell(7, emails_val)

        # Col 8 — Google Maps
        maps_url = safe(business.maps_url)
        write_cell(
            8,
            "View on Maps" if maps_url != "N/A" else "N/A",
            hyperlink=maps_url if maps_url != "N/A" else None,
            align=center
        )

        # Col 9 — Facebook
        fb = safe(business.facebook)
        write_cell(9, fb, hyperlink=fb if fb != "N/A" else None)

        # Col 10 — Instagram
        ig = safe(business.instagram)
        write_cell(10, ig, hyperlink=ig if ig != "N/A" else None)

        # Col 11 — LinkedIn
        li = safe(business.linkedin)
        write_cell(11, li, hyperlink=li if li != "N/A" else None)

        # Col 12 — YouTube
        yt = safe(business.youtube)
        write_cell(12, yt, hyperlink=yt if yt != "N/A" else None)

        ws.row_dimensions[row_idx].height = 18

    # ── Auto-size columns ────────────────────────────────
    for col in range(1, len(headers) + 1):

        letter = get_column_letter(col)
        max_length = 0

        for row in range(2, ws.max_row + 1):

            value = ws.cell(row=row, column=col).value

            if value is None:
                continue

            max_length = max(max_length, len(str(value)))

        ws.column_dimensions[letter].width = min(max_length + 3, 55)

    # ── Freeze panes & filter ────────────────────────────
    ws.freeze_panes      = "A3"
    ws.auto_filter.ref   = (
        f"A2:{get_column_letter(len(headers))}{len(export_list) + 2}"
    )

    # ── Open on Summary sheet ────────────────────────────
    # wb.active must be an integer sheet index, not a Worksheet object.
    # Summary is inserted at index 0 by add_summary_sheet().
    wb.active = 0

    wb.save(filename)