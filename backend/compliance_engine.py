import json
import os
from datetime import datetime, date

from translation_map import translation_map, translate_term

# paths to data and mock uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGULATIONS_FILE = os.path.join(BASE_DIR, "data", "regulations.json")
MOCK_UPLOADS_DIR = os.path.join(BASE_DIR, "mock_uploads")


def load_regulations():
    # load the source of truth json file
    with open(REGULATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


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


def check_compliance(producer_data):
    """
    Core gap analysis function per task 3 spec.

    Args:
        producer_data: dict with product, destination, current_date, uploaded_docs

    Returns:
        dict with full compliance result including missing documents
    """
    # step 1 accept input for product, destination, and current_date
    product = producer_data.get("product", "")
    destination = producer_data.get("destination", "")
    date_str = producer_data.get("current_date", str(date.today()))
    uploaded_raw = producer_data.get("uploaded_docs", [])

    # step 2 load regulations.json and retrieve required doc list
    regulations = load_regulations()
    country_data = regulations.get(destination, {})
    product_data = country_data.get(product, {})

    if not product_data:
        return {
            "status": "ERROR",
            "message": f"no data found for '{product}' in '{destination}'",
            "product": product,
            "destination": destination
        }

    required_docs = product_data.get("required_docs", [])

    # translate uploaded filenames from spanish to english before comparing
    translated_uploads = [translate_term(doc).lower().strip() for doc in uploaded_raw]

    # step 3 compare required list against uploaded list
    missing_docs = []
    received_docs = []

    for req in required_docs:
        req_normalized = req.lower().strip()
        matched = any(
            req_normalized in uploaded or uploaded in req_normalized
            for uploaded in translated_uploads
        )
        if matched:
            received_docs.append(req)
        else:
            missing_docs.append(req)

    gap_count = len(missing_docs)

    # step 4 check current_date against seasonal duty windows
    try:
        shipment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        shipment_date = date.today()

    seasonal_result = get_seasonal_duty(product_data, shipment_date)

    # determine final compliance status
    if gap_count == 0:
        compliance_status = "READY — all required documents present"
    elif gap_count <= 2:
        compliance_status = "ACTION REQUIRED — missing some documents"
    else:
        compliance_status = "ACTION REQUIRED — missing critical documents"

    return {
        "product": product,
        "destination": destination,
        "shipment_date": str(shipment_date),
        "hts_code": product_data.get("hts_code", product_data.get("hs_code", "")),
        "base_duty": product_data.get("base_duty", ""),
        "applicable_duty": seasonal_result["duty"],
        "applicable_subheading": seasonal_result["subheading"],
        "seasonal_period": seasonal_result["period"],
        "seasonal_applied": seasonal_result["seasonal_applied"],
        "required_docs": required_docs,
        "uploaded_docs_raw": uploaded_raw,
        "uploaded_docs_translated": [translate_term(d) for d in uploaded_raw],
        "received_docs": received_docs,
        "missing_docs": missing_docs,
        "gap_count": gap_count,
        "compliance_status": compliance_status
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
    for test in test_cases:
        result = check_compliance(test)
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
    print(f"\n  report saved to: validation_report.txt")