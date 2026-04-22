import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from compliance_engine import run_tests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "Compliance_Gap_Report.pdf")


def clean_text(text):
    # replace unicode characters that core pdf fonts do not support
    replacements = {
        "—": "-",
        "–": "-",
        "→": "->",
        "✓": "[OK]",
        "✗": "[MISSING]",
        "⚠": "[ALERT]",
        "’": "'",
        "“": '"',
        "”": '"',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(
            0,
            10,
            "CultiveConnect - Compliance Gap Validation Report",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
        )
        self.ln(4)

    def add_section_title(self, title):
        self.set_font("helvetica", "B", 12)
        self.cell(
            0,
            8,
            clean_text(title),
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.ln(1)

    def add_body_text(self, text):
        self.set_font("helvetica", "", 11)
        self.multi_cell(0, 7, clean_text(text))
        self.ln(2)


def build_result_text(result):
    lines = []
    lines.append(f"Product: {result['product']}")
    lines.append(f"Destination: {result['destination']}")
    lines.append(f"Shipment Date: {result['shipment_date']}")
    lines.append(f"HTS Code: {result['hts_code']}")
    lines.append(f"Base Duty: {result['base_duty']}")
    lines.append(f"Applicable Duty: {result['applicable_duty']}")
    lines.append(f"Seasonal Period: {result['seasonal_period']}")
    lines.append(f"Seasonal Applied: {'Yes' if result['seasonal_applied'] else 'No'}")
    lines.append("")

    lines.append("Required Documents:")
    for doc in result["required_docs"]:
        lines.append(f"  - {doc}")
    lines.append("")

    lines.append("Uploaded Documents:")
    for orig, translated in zip(result["uploaded_docs_raw"], result["uploaded_docs_translated"]):
        if orig != translated:
            lines.append(f"  - {orig} -> {translated}")
        else:
            lines.append(f"  - {orig}")
    lines.append("")

    lines.append("Received Documents:")
    if result["received_docs"]:
        for doc in result["received_docs"]:
            lines.append(f"  - {doc}")
    else:
        lines.append("  - None")
    lines.append("")

    lines.append("Missing Documents:")
    if result["missing_docs"]:
        for doc in result["missing_docs"]:
            lines.append(f"  - {doc}")
    else:
        lines.append("  - None")
    lines.append("")

    lines.append(f"Compliance Status: {result['compliance_status']}")

    return "\n".join(lines)


def main():
    results = run_tests()

    # only keep products with actual compliance gaps
    gap_results = [r for r in results if r.get("gap_count", 0) > 0]

    # take first two products with gaps
    selected_results = gap_results[:2]

    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_section_title("Validation Summary")
    pdf.add_body_text(
        "This PDF export shows the compliance engine correctly identifying document gaps "
        "for at least two different products using the mock testing suite."
    )

    for i, result in enumerate(selected_results, 1):
        pdf.add_section_title(f"Test Case {i}: {result['product']} -> {result['destination']}")
        pdf.add_body_text(build_result_text(result))

    pdf.output(OUTPUT_FILE)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()