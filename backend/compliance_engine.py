import json
import os
from datetime import datetime

from translation_map import translation_map, translate_term

# paths to data and mock uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGULATIONS_FILE = os.path.join(BASE_DIR, "data", "regulations.json")
MOCK_UPLOADS_DIR = os.path.join(BASE_DIR, "mock_uploads")


def load_regulations():
    # load the source of truth json file
    with open(REGULATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_uploaded_filenames(uploaded_filenames):
    # turns textarea input into a clean list of filenames
    if not uploaded_filenames:
        return []

    if isinstance(uploaded_filenames, list):
        return [f.strip() for f in uploaded_filenames if str(f).strip()]

    cleaned = uploaded_filenames.replace("\n", ",")
    files = [f.strip() for f in cleaned.split(",") if f.strip()]
    return files


def scan_mock_uploads():
    # read all pdf filenames from mock_uploads folder
    if not os.path.exists(MOCK_UPLOADS_DIR):
        return []

    results = []
    for filename in os.listdir(MOCK_UPLOADS_DIR):
        if filename.lower().endswith(".pdf"):
            # translate spanish filenames to english using task 2
            translated = translate_term(filename)
            results.append({
                "original_filename": filename,
                "translated_name": translated,
                "status": "Received"
            })
    return results


def get_seasonal_duty(product_data, shipment_date):
    # check if seasonal adjustment applies for this product
    seasonal = product_data.get("seasonal_adjustment", {})

    if not seasonal.get("applies", False):
        # no seasonal window so return base duty year round
        return {
            "duty": product_data.get("base_duty", "See regulations"),
            "subheading": product_data.get("hts_code", product_data.get("hs_code", "")),
            "period": "Year-round",
            "seasonal_applied": False
        }

    # step 4 compare shipment date against seasonal windows using if/else
    windows = seasonal.get("windows", [])

    for window in windows:
        period = window["period"]
        parts = period.split(" to ")

        if len(parts) == 2:
            try:
                # include the year directly to avoid the date parsing warning
                start_str = f"{parts[0].strip()} {shipment_date.year}"
                end_str = f"{parts[1].strip()} {shipment_date.year}"

                start = datetime.strptime(start_str, "%B %d %Y")
                end = datetime.strptime(end_str, "%B %d %Y")

                # handle windows that wrap across year end
                if start.date() <= end.date():
                    in_window = start.date() <= shipment_date <= end.date()
                else:
                    in_window = shipment_date >= start.date() or shipment_date <= end.date()

                if in_window:
                    return {
                        "duty": window["duty"],
                        "subheading": window["subheading"],
                        "period": period,
                        "seasonal_applied": True
                    }
            except ValueError:
                continue

    # no window matched so fall back to base duty
    return {
        "duty": product_data.get("base_duty", "See regulations"),
        "subheading": product_data.get("hts_code", product_data.get("hs_code", "")),
        "period": "Outside defined windows",
        "seasonal_applied": False
    }


def check_seasonal_alerts(result):
    # build a farmer friendly seasonal alert message
    if not result.get("seasonal_applied", False):
        return None

    product = result.get("product", "")
    destination = result.get("destination", "")
    shipment_date = result.get("shipment_date", "")
    seasonal_period = result.get("seasonal_period", "")
    applicable_duty = result.get("applicable_duty", "")
    base_duty = result.get("base_duty", "")
    subheading = result.get("applicable_subheading", "")

    lines = []
    lines.append(f"⚠ SEASONAL ALERT — {product} to {destination}")
    lines.append(
        f"Your shipment date ({shipment_date}) falls in the seasonal window ({seasonal_period})."
    )

    if applicable_duty != base_duty:
        lines.append(f"Duty rate: {applicable_duty} instead of {base_duty}.")
    else:
        lines.append(f"Seasonal rules apply during this period. Current duty rate: {applicable_duty}.")

    if subheading:
        lines.append(f"Use tariff subheading: {subheading}.")

    if product.lower() == "asparagus":
        lines.append("Review the shipment date in case an earlier shipment avoids seasonal restrictions.")
    elif product.lower() == "grapes":
        lines.append("Make sure the seasonal subheading is used on the entry paperwork.")

    return "\n".join(lines)


def check_compliance(producer_data, regulations_data=None):
    # load regulations if not passed in
    if regulations_data is None:
        regulations_data = load_regulations()

    destination = producer_data["destination"]
    product = producer_data["product"]

    # support both keys just in case
    shipment_date_str = producer_data.get("shipment_date", producer_data.get("current_date"))
    uploaded_input = producer_data.get("uploaded_filenames", producer_data.get("uploaded_docs", []))

    try:
        shipment_date = datetime.strptime(shipment_date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            shipment_date = datetime.strptime(shipment_date_str, "%m/%d/%Y").date()
        except ValueError:
            return {
                "product": product,
                "destination": destination,
                "status": "ERROR",
                "message": f"Invalid date format: {shipment_date_str}"
            }

    # validate destination and product
    if destination not in regulations_data:
        return {
            "product": product,
            "destination": destination,
            "status": "ERROR",
            "message": f"Destination '{destination}' not found in regulations."
        }

    if product not in regulations_data[destination]:
        return {
            "product": product,
            "destination": destination,
            "status": "ERROR",
            "message": f"Product '{product}' not found under destination '{destination}'."
        }

    # get product rules
    product_data = regulations_data[destination][product]
    required_docs = product_data.get("required_docs", [])

    # parse filenames correctly
    uploaded_files = parse_uploaded_filenames(uploaded_input)

    # translate every uploaded filename
    translated_files = [translate_term(f) for f in uploaded_files]

    # match translated filenames against required docs
    received_docs = [doc for doc in required_docs if doc in translated_files]
    missing_docs = [doc for doc in required_docs if doc not in translated_files]

    # coverage
    coverage = int((len(received_docs) / len(required_docs)) * 100) if required_docs else 0

    # status
    if coverage == 100:
        compliance_status = "READY"
    elif coverage == 0:
        compliance_status = "CRITICAL GAPS"
    else:
        compliance_status = "ACTION REQUIRED"

    # seasonal duty logic
    seasonal_info = get_seasonal_duty(product_data, shipment_date)

    return {
        "product": product,
        "destination": destination,
        "shipment_date": shipment_date.strftime("%Y-%m-%d"),
        "hts_code": product_data.get("hts_code", product_data.get("hs_code", "")),
        "base_duty": product_data.get("base_duty", "See regulations"),
        "applicable_duty": seasonal_info["duty"],
        "applicable_subheading": seasonal_info["subheading"],
        "seasonal_period": seasonal_info["period"],
        "seasonal_applied": seasonal_info["seasonal_applied"],
        "required_docs": required_docs,
        "uploaded_docs_raw": uploaded_files,
        "uploaded_docs_translated": translated_files,
        "received_docs": received_docs,
        "missing_docs": missing_docs,
        "gap_count": len(missing_docs),
        "coverage": coverage,
        "compliance_status": compliance_status,
        "status": compliance_status
    }


def run_tests():
    # scan mock_uploads folder and collect uploaded filenames
    uploaded_files = scan_mock_uploads()
    uploaded_names = [f["original_filename"] for f in uploaded_files]

    print(f"\n  found {len(uploaded_files)} files in mock_uploads/:")
    for f in uploaded_files:
        print(f"    {f['original_filename']} → {f['translated_name']} [{f['status']}]")

    # test cases covering grapes vs coffee as required by spec
    test_cases = [
        {
            "product": "Grapes",
            "destination": "USA",
            "current_date": "2026-03-19",
            "uploaded_docs": uploaded_names
        },
        {
            "product": "Coffee_Green",
            "destination": "USA",
            "current_date": "2026-03-19",
            "uploaded_docs": uploaded_names
        },
        {
            "product": "Asparagus",
            "destination": "Canada",
            "current_date": "2026-06-20",
            "uploaded_docs": uploaded_names
        },
        {
            "product": "Quinoa",
            "destination": "USA",
            "current_date": "2026-03-19",
            "uploaded_docs": []
        },
    ]

    results = []
    regulations_data = load_regulations()

    for test in test_cases:
        result = check_compliance(test, regulations_data)
        results.append(result)

    return results


def generate_report(results):
    # build the validation report showing gaps for each product
    lines = []
    lines.append("=" * 60)
    lines.append("  cultiveconnect — compliance validation report")
    lines.append(f"  generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    for i, result in enumerate(results, 1):
        lines.append(f"\n  {'─' * 56}")
        lines.append(f"  test {i}: {result['product']} → {result['destination']}")
        lines.append(f"  {'─' * 56}")

        if result.get("status") == "ERROR":
            lines.append(f"  error: {result.get('message')}")
            continue

        lines.append(f"  shipment date:     {result['shipment_date']}")
        lines.append(f"  hts code:          {result['hts_code']}")
        lines.append(f"  base duty:         {result['base_duty']}")
        lines.append(f"  applicable duty:   {result['applicable_duty']}")
        lines.append(f"  seasonal period:   {result['seasonal_period']}")
        lines.append(f"  seasonal applied:  {'yes' if result['seasonal_applied'] else 'no'}")
        lines.append(f"  coverage:          {result['coverage']}%")

        alert = check_seasonal_alerts(result)
        if alert:
            lines.append("")
            for line in alert.split("\n"):
                lines.append(f"  {line}")

        lines.append("")
        lines.append(f"  required docs ({len(result['required_docs'])}):")
        for doc in result["required_docs"]:
            lines.append(f"    - {doc}")

        lines.append("")
        lines.append(f"  uploaded docs ({len(result['uploaded_docs_raw'])}):")
        for orig, translated in zip(result["uploaded_docs_raw"], result["uploaded_docs_translated"]):
            if orig != translated:
                lines.append(f"    - {orig}  →  {translated}")
            else:
                lines.append(f"    - {orig}")

        lines.append("")
        lines.append(f"  received ({len(result['received_docs'])}):")
        for doc in result["received_docs"]:
            lines.append(f"    ✓  {doc}")

        lines.append("")
        lines.append(f"  missing ({result['gap_count']}):")
        if result["missing_docs"]:
            for doc in result["missing_docs"]:
                lines.append(f"    ✗  {doc}")
        else:
            lines.append("    none — all documents present")

        lines.append("")
        lines.append(f"  status: {result['compliance_status']}")

    lines.append(f"\n  {'=' * 58}")
    lines.append("  end of report")
    lines.append("=" * 60)

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("  task 3 — gap analysis engine")
    print("=" * 60)

    results = run_tests()
    report = generate_report(results)
    print(report)

    # save report to file
    report_path = os.path.join(BASE_DIR, "validation_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n  report saved to: {report_path}")