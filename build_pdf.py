import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.pdfgen import canvas

PDF_PATH = "d:/PM_PRJ/GitHub_QA_Report_Parshva_Dongare.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A4

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer()
            super().showPage()
        super().save()

    def draw_header_footer(self):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.black)
        # Top running header
        header_text = f"GitHub QA Report | Page {self._pageNumber}"
        self.drawRightString(PAGE_WIDTH - 40, PAGE_HEIGHT - 30, header_text)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    # Custom styles - all text in pure black (#000000)
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.black,
        alignment=1, # Center
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=12,
        leading=16,
        textColor=colors.black,
        alignment=1, # Center
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=colors.black
    )

    h1_style = ParagraphStyle(
        "H1Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        "H2Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.black,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        "BodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.black
    )

    caption_style = ParagraphStyle(
        "CaptionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11,
        textColor=colors.black,
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        textColor=colors.black,
        backColor=colors.HexColor("#F4F6F8"),
        borderColor=colors.HexColor("#D0D7DE"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5
    )

    story = []

    # Helper for image insertion
    def add_fig(num, caption, height=185):
        img_path = f"d:/PM_PRJ/screenshots/figure_{num}.png"
        if os.path.exists(img_path):
            img = RLImage(img_path, width=500, height=height)
            story.append(img)
            story.append(Paragraph(f"Figure {num}: {caption}", caption_style))

    # =========================================================================
    # PAGE 1
    # =========================================================================
    story.append(Paragraph("GitHub-Based QA Documentation and Problem Solving", title_style))
    story.append(Paragraph("Case study: Smart Environmental Air Quality & Toxic Gas Alert Monitor", subtitle_style))

    meta_text = """
    <b>Name</b> – Parshva Dongare<br/>
    <b>PRN</b> – 202301070033<br/>
    <b>Class</b> – A
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("A. GitHub Repository Link", h1_style))
    repo_links = """
    <b>Repository:</b> <font color="#000000"><u>https://github.com/ParshvaDongare/Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor</u></font><br/>
    <b>Pull request:</b> <font color="#000000"><u>https://github.com/ParshvaDongare/Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor/pull/1</u></font><br/>
    <b>Project board:</b> Air Quality Monitor QA Tracker (GitHub Projects)
    """
    story.append(Paragraph(repo_links, body_style))
    story.append(Paragraph("The repository was created with a README and an MIT licence, with Issues and Projects enabled.", body_style))
    story.append(Spacer(1, 4))

    add_fig(1, "Repository home page (Smart-Environmental-Air-Quality-Toxic-Gas-Alert-Monitor)", height=170)

    story.append(Paragraph("B. Brief Description of Code", h1_style))
    story.append(Paragraph("The project monitors ambient toxic gases (MQ-135) and temperature/humidity (DHT22) using an Arduino Uno, displaying status on an I2C LCD and triggering acoustic/optical alerts. It was developed in two versions so that real quality problems could be found, logged on GitHub and fixed.", body_style))
    story.append(Paragraph("Version 1 (initial commit)", h2_style))
    story.append(Paragraph("A basic sketch using hard-coded pin and timing values and blocking delay() calls, with no warmup delay and a default README.", body_style))

    v1_code_p1 = """void setup() {<br/>
&nbsp;&nbsp;pinMode(2, INPUT_PULLUP); // Mute button<br/>
&nbsp;&nbsp;pinMode(8, OUTPUT);       // Active Buzzer<br/>
&nbsp;&nbsp;Wire.begin();             // No I2C timeout<br/>
&nbsp;&nbsp;lcd.init();<br/>
&nbsp;&nbsp;dht.begin();<br/>
}"""
    story.append(Paragraph(v1_code_p1, code_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2
    # =========================================================================
    v1_code_p2 = """void loop() {<br/>
&nbsp;&nbsp;int rawADC = analogRead(A0);<br/>
&nbsp;&nbsp;float ppm = (rawADC * 5.0 / 1023.0) * 200.0;<br/>
&nbsp;&nbsp;if (digitalRead(2) == LOW) { alarmMuted = !alarmMuted; } // No debounce<br/>
&nbsp;&nbsp;if (ppm > 500 && !alarmMuted) { digitalWrite(8, HIGH); } // No warmup check<br/>
&nbsp;&nbsp;else { digitalWrite(8, LOW); }<br/>
&nbsp;&nbsp;delay(2000); // Blocking delay halts loop & delays emergency alerts<br/>
}"""
    story.append(Paragraph(v1_code_p2, code_style))

    add_fig(2, "Smart_Air_Quality_Monitor.ino v1 committed to the main branch", height=185)

    story.append(Paragraph("Version 2 (after QA fixes)", h2_style))
    story.append(Paragraph("Named constants in Config.h replace magic numbers, a non-blocking millis() timer replaces delay(), a 30s warmup timer prevents false alarms on boot, 50ms software debounce stabilizes the mute switch, I2C bus timeout protects against hangs, and serial messages at 9600 baud allow behaviour verification. The README now has components, wiring, upload steps, expected output and test results.", body_style))

    v2_code = """const int LED_PIN = 13;<br/>
const unsigned long INTERVAL_GAS_SAMPLE_MS = 100;<br/>
unsigned long lastGasSampleTimestamp = 0;<br/>
<br/>
void loop() {<br/>
&nbsp;&nbsp;unsigned long currentMillis = millis();<br/>
&nbsp;&nbsp;// Task 1: Non-blocking button debounce filter<br/>
&nbsp;&nbsp;handleButtonDebounce(currentMillis);<br/>
&nbsp;&nbsp;// Task 2: 30s Sensor warmup countdown state machine<br/>
&nbsp;&nbsp;if (!sensorReady) { handleWarmupCountdown(currentMillis); return; }<br/>
&nbsp;&nbsp;// Task 3: 10 Hz gas sampling for instantaneous alert response<br/>
&nbsp;&nbsp;if (currentMillis - lastGasSampleTimestamp >= INTERVAL_GAS_SAMPLE_MS) {<br/>
&nbsp;&nbsp;&nbsp;&nbsp;lastGasSampleTimestamp = currentMillis;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;cachedPpm = readGasPpm();<br/>
&nbsp;&nbsp;&nbsp;&nbsp;actuateAlarms(cachedPpm);<br/>
&nbsp;&nbsp;}<br/>
}"""
    story.append(Paragraph(v2_code, code_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3
    # =========================================================================
    add_fig(3, "Smart_Air_Quality_Monitor.ino v2 on the fix/improve-code-and-docs branch", height=185)
    add_fig(4, "Updated README with components, wiring and test results", height=185)

    story.append(Paragraph("Circuit", h2_style))
    circuit_data = [
        [Paragraph("<b>From</b>", body_style), Paragraph("<b>To</b>", body_style)],
        [Paragraph("Arduino pin A0", body_style), Paragraph("MQ-135 Gas Sensor Analog Output (AOUT)", body_style)],
        [Paragraph("Arduino pin A4 (SDA)", body_style), Paragraph("16x2 I2C LCD SDA (with 4.7k ohm pull-up to 5V)", body_style)],
        [Paragraph("Arduino pin A5 (SCL)", body_style), Paragraph("16x2 I2C LCD SCL (with 4.7k ohm pull-up to 5V)", body_style)],
        [Paragraph("Arduino pin D2", body_style), Paragraph("Pushbutton terminal (Mute toggle, other pin to GND)", body_style)],
        [Paragraph("Arduino pin D4", body_style), Paragraph("DHT22 Single-Wire Data pin (with 10k ohm pull-up)", body_style)],
        [Paragraph("Arduino pin D8", body_style), Paragraph("Active Piezo Buzzer Positive Terminal", body_style)],
        [Paragraph("Arduino pin D9 / D10", body_style), Paragraph("Red / Green LEDs Anodes (via 220 ohm resistors)", body_style)],
    ]
    c_table = Table(circuit_data, colWidths=[160, 340])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F4F7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(c_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4
    # =========================================================================
    story.append(Paragraph("C. QA Issues Logged", h1_style))
    story.append(Paragraph("Five issues were logged using GitHub Issues. Each has a description, expected and actual behaviour, steps to reproduce, a severity, labels, and a root cause analysis comment.", body_style))
    story.append(Spacer(1, 4))

    issues_data = [
        [Paragraph("<b>#</b>", body_style), Paragraph("<b>Issue title</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Severity</b>", body_style), Paragraph("<b>Labels</b>", body_style)],
        ["1", Paragraph("No warmup delay for MQ-135 causing false alarm", body_style), "Hardware", "High", "bug, hardware"],
        ["2", Paragraph("Pin assignments and thresholds hard-coded", body_style), "Code quality", "Low", "enhancement"],
        ["3", Paragraph("I2C bus lockup and MCU freeze under noise", body_style), "Design / bug", "Critical", "bug, hardware"],
        ["4", Paragraph("Switch contact bounce causes double-toggle on mute", body_style), "Hardware", "Medium", "bug, hardware"],
        ["5", Paragraph("Blocking delay() prevents multitasking & fast alert", body_style), "Design / bug", "High", "bug, enhancement"],
    ]
    i_table = Table(issues_data, colWidths=[20, 200, 80, 65, 135])
    i_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F4F7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(i_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Custom labels", h2_style))
    story.append(Paragraph("Labels (hardware, documentation, enhancement, testing, plus the default bug) were used to categorise the issues.", body_style))

    add_fig(5, "Labels used to categorise issues", height=155)

    story.append(Paragraph("Root cause analysis", h2_style))
    story.append(Paragraph("<b>Issue #1 (5-Why):</b> Buzzer activates immediately on boot, because MQ-135 reads over 500 PPM; the internal heater coil has not reached 300°C operating temperature; the firmware evaluated readings immediately in setup(); the code assumed sensor output was valid instantaneously; there was no hardware checklist in the template. Root cause: no startup stabilization/warmup timer standard.", body_style))
    story.append(Paragraph("<b>Issue #3 (5-Why & Fishbone):</b> The CPU is trapped inside Wire library; dropped ACK pulse caused by electrical noise and jumper wire capacitance; missing 4.7k external pull-up resistors; default Wire library lacked timeout protection. Root cause: missing bus pull-ups and lack of bus timeout safeguards.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5
    # =========================================================================
    story.append(Paragraph("Issues #2, #4, #5: a short cause and fix plan was recorded for each (no embedded coding standard established initially, mechanical contact bounce on tactile switches not filtered, and synchronous procedural design blocking the main CPU loop).", body_style))
    story.append(Spacer(1, 4))

    add_fig(6, "Issue #1 with labels and 5-Why root cause comment", height=195)
    add_fig(7, "Issue #2: hard-coded values, with cause and fix plan", height=195)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6
    # =========================================================================
    add_fig(8, "Issue #3 with 5-Why root cause comment", height=210)
    add_fig(9, "Issue #4: switch bounce, with 5-Why root cause comment", height=210)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7
    # =========================================================================
    add_fig(10, "Issue #5: blocking delay, with 5-Why root cause comment", height=205)

    story.append(Paragraph("Resolution log", h2_style))
    story.append(Paragraph("After the pull request was merged, all five issues closed automatically through the \"Fixes #n\" references.", body_style))

    add_fig(11, "All five issues closed after the merge", height=185)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8
    # =========================================================================
    story.append(Paragraph("D. Collaboration Summary", h1_style))
    story.append(Paragraph("GitHub features used: Issues, Labels, Branches, Commits, Pull Requests with review comments, Milestones and Projects.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Branching", h2_style))
    story.append(Paragraph("The branch fix/improve-code-and-docs was created from main so that main stayed stable while the fixes were developed.", body_style))

    add_fig(12, "New branch created from main", height=170)
    add_fig(13, "Branches page showing main and the fix branch", height=170)

    story.append(Paragraph("2. Pull request", h2_style))
    story.append(Paragraph("Pull request #1, \"Fix QA issues: improve code, non-blocking scheduler, and documentation (v2)\", contained four commits and referenced Fixes #1 to #5. GitHub linked each issue to the pull request automatically.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9
    # =========================================================================
    add_fig(14, "Pull request #1: description, linked issues and commits", height=195)

    story.append(Paragraph("3. Review and discussion", h2_style))
    story.append(Paragraph("This was an individual activity and no external reviewer was available, so a self-review was carried out. A line comment on Smart_Air_Quality_Monitor.ino confirmed that millis() replaces delay() so the loop is no longer blocked, the conversation was resolved, and a self-review and test summary was posted on the pull request.", body_style))

    add_fig(15, "Line comment on the code change in the pull request", height=180)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10
    # =========================================================================
    add_fig(16, "Self-review and test summary; no merge conflicts", height=190)

    story.append(Paragraph("4. Merge", h2_style))
    add_fig(17, "Pull request merged and closed", height=190)

    story.append(Paragraph("After the merge, the fix branch was deleted and only main remained.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11
    # =========================================================================
    add_fig(18, "Branch deleted after the merge", height=155)
    add_fig(19, "Only the main branch remains", height=140)

    story.append(Paragraph("5. Commit history", h2_style))
    commits_data = [
        [Paragraph("<b>Commit</b>", body_style), Paragraph("<b>Message</b>", body_style), Paragraph("<b>Purpose</b>", body_style)],
        ["6cde1ff", "feat: initial prototype of air quality monitor and project docs", "Repository setup & v1 code"],
        ["a5b4edb", "docs: add QA test plan, root cause analysis, and project tracking", "QA test matrices and docs"],
        ["ce6f752", "fix(firmware): resolve QA-001 false alarm during warmup cycle", "Fixes #1 (Sensor warmup)"],
        ["99b967b", "fix(driver): configure I2C wire timeout and peripheral auto-recovery", "Fixes #3 (I2C bus timeout)"],
        ["abe5547", "fix(input): implement 50ms software debounce for mute switch", "Fixes #4 (Button debounce)"],
        ["b84649f", "refactor(core): replace blocking delays with cooperative non-blocking FSM", "Fixes #2, #5 (FSM scheduler)"],
        ["abfc080", "Merge pull request #1 from fix/improve-code-and-docs", "Merge into main"],
    ]
    cmt_table = Table(commits_data, colWidths=[65, 305, 130])
    cmt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F4F7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(cmt_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12
    # =========================================================================
    add_fig(20, "Commit history on the main branch", height=180)

    story.append(Paragraph("E. Learning Outcome", h1_style))
    learnings = [
        "• GitHub Issues give traceability from a problem, to its root cause, to the commit that fixed it.",
        "• Branches and pull requests keep the main code stable and make every change reviewable.",
        "• Writing \"Fixes #n\" in the pull request closed the issues automatically and produced a resolution log.",
        "• The 5-Why method showed that the causes were process gaps, such as missing QA standards and requirements, and not only code errors.",
        "• In embedded projects hardware documentation, such as the pull-up resistor value and wiring, is as important as the code.",
        "• Milestones and project boards make progress visible to everyone on the project."
    ]
    for l in learnings:
        story.append(Paragraph(l, body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Pre-reflection", h2_style))
    story.append(Paragraph("Collaborative platforms like GitHub can improve transparency and traceability by keeping every defect, discussion and fix in one place.", body_style))

    story.append(Paragraph("Post-reflection", h2_style))
    story.append(Paragraph("GitHub made the documentation structured and the issue resolution visible, and it linked every fix to its problem. The pull request workflow would be even more valuable with a real peer reviewer.", body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("F. Report Upload", h1_style))
    story.append(Paragraph("This report is exported as a PDF with the screenshots and uploaded to Moodle for the course Project Management.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13
    # =========================================================================
    story.append(Paragraph("G. Project Planning and Tracking", h1_style))
    story.append(Paragraph("Plan and status", h2_style))

    plan_data = [
        [Paragraph("<b>Task</b>", body_style), Paragraph("<b>Date</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        ["Repository setup and v1 code", "18 Nov 2026", "Done"],
        ["Log QA issues with root cause analysis", "18 Nov 2026", "Done"],
        ["Fix on branch, update README, open pull request", "18 Nov 2026", "Done"],
        ["Self-review, merge and close issues", "18 Nov 2026", "Done"],
        ["Milestone, project board and report", "18 Nov 2026", "Done"],
    ]
    p_table = Table(plan_data, colWidths=[270, 110, 120])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F4F7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Milestone: v1.0 Release", h2_style))
    story.append(Paragraph("All 5 issues were assigned to the milestone \"v1.0 Release\" (due 19 November 2026). It shows 100% complete with 0 open and 5 closed issues.", body_style))

    add_fig(21, "Milestone v1.0 Release at 100%", height=170)

    story.append(Paragraph("Project board: Air Quality Monitor QA Tracker", h2_style))
    story.append(Paragraph("A board with Todo, In Progress and Done columns tracks the work. Issues #1 to #5 and pull request #1 are in the Done column.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14
    # =========================================================================
    add_fig(22, "Project board with all items in Done", height=230)

    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("Using GitHub for a small embedded project showed how issue tracking, root cause analysis, branching, pull requests, milestones and project boards support quality assurance and teamwork. All five logged issues were analysed, fixed and closed with a complete trail of evidence.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete: 14 pages generated successfully!")

if __name__ == "__main__":
    build_pdf()
