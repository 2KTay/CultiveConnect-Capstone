# maps spanish document names and product names to english equivalents
translation_map = {

    # document types
    "Certificado Fitosanitario":          "Phytosanitary Certificate",
    "certificado_fitosanitario":          "Phytosanitary Certificate",
    "certificado fitosanitario":          "Phytosanitary Certificate",
    "CertificadoFitosanitario":           "Phytosanitary Certificate",

    "Aviso Previo FDA":                   "FDA Prior Notice",
    "aviso_previo_fda":                   "FDA Prior Notice",
    "aviso previo fda":                   "FDA Prior Notice",
    "Aviso Previo":                       "FDA Prior Notice",
    "aviso_previo":                       "FDA Prior Notice",

    "Registro de Instalacion FDA":        "FDA Food Facility Registration",
    "registro_instalacion_fda":           "FDA Food Facility Registration",
    "registro de instalacion fda":        "FDA Food Facility Registration",
    "Registro Instalacion FDA":           "FDA Food Facility Registration",
    "Registro de Establecimiento":        "FDA Food Facility Registration",

    "Inspeccion en Puerto de Entrada":    "Port of Entry Inspection",
    "inspeccion_puerto_entrada":          "Port of Entry Inspection",
    "inspeccion en puerto de entrada":    "Port of Entry Inspection",
    "Inspeccion Portuaria":               "Port of Entry Inspection",
    "inspeccion_portuaria":               "Port of Entry Inspection",

    "Verificacion AIRS":                  "AIRS Verification",
    "verificacion_airs":                  "AIRS Verification",
    "verificacion airs":                  "AIRS Verification",
    "Verificacion CFIA":                  "AIRS Verification",

    "Factura Comercial":                  "Commercial Invoice",
    "factura_comercial":                  "Commercial Invoice",
    "factura comercial":                  "Commercial Invoice",
    "Factura de Exportacion":             "Commercial Invoice",
    "factura_de_exportacion":             "Commercial Invoice",

    "Lista de Empaque":                   "Packing List",
    "lista_de_empaque":                   "Packing List",
    "lista de empaque":                   "Packing List",
    "Lista de Embalaje":                  "Packing List",
    "lista_de_embalaje":                  "Packing List",

    "Certificado de Origen":              "Certificate of Origin",
    "certificado_de_origen":              "Certificate of Origin",
    "certificado de origen":              "Certificate of Origin",

    "Conocimiento de Embarque":           "Bill of Lading",
    "conocimiento_de_embarque":           "Bill of Lading",
    "conocimiento de embarque":           "Bill of Lading",
    "Guia de Embarque":                   "Bill of Lading",
    "guia_de_embarque":                   "Bill of Lading",

    "Permiso de Exportacion":             "Export Permit",
    "permiso_de_exportacion":             "Export Permit",
    "permiso de exportacion":             "Export Permit",

    "Certificado de Fumigacion":          "Fumigation Certificate",
    "certificado_de_fumigacion":          "Fumigation Certificate",
    "certificado de fumigacion":          "Fumigation Certificate",

    "Certificado Sanitario":              "Health Certificate",
    "certificado_sanitario":              "Health Certificate",
    "certificado sanitario":              "Health Certificate",

    # product names — matches carlos spec examples exactly
    "Arandanos":                          "Blueberries",
    "arandanos":                          "Blueberries",
    "Arándanos":                          "Blueberries",
    "arándanos":                          "Blueberries",
    "Mirtilo":                            "Blueberries",
    "mirtilo":                            "Blueberries",

    "Esparragos":                         "Asparagus",
    "esparragos":                         "Asparagus",
    "Espárragos":                         "Asparagus",
    "espárragos":                         "Asparagus",

    "Uvas":                               "Grapes",
    "uvas":                               "Grapes",
    "Uvas Frescas":                       "Grapes",
    "uvas_frescas":                       "Grapes",

    "Cafe Verde":                         "Coffee_Green",
    "cafe_verde":                         "Coffee_Green",
    "cafe verde":                         "Coffee_Green",
    "Café Verde":                         "Coffee_Green",
    "Cafe Sin Tostar":                    "Coffee_Green",

    "Cafe Tostado":                       "Coffee_Roasted",
    "cafe_tostado":                       "Coffee_Roasted",
    "cafe tostado":                       "Coffee_Roasted",
    "Café Tostado":                       "Coffee_Roasted",

    "Quinua":                             "Quinoa",
    "quinua":                             "Quinoa",
    "Quinoa":                             "Quinoa",

    # country names
    "Estados Unidos":                     "USA",
    "estados_unidos":                     "USA",
    "EE.UU.":                             "USA",
    "Canada":                             "Canada",
    "Canadá":                             "Canada",
}


def translate_term(term: str) -> str:
    # strip file extension before lookup
    clean = term.replace(".pdf", "").replace(".PDF", "").strip()

    # try exact match first
    if clean in translation_map:
        return translation_map[clean]

    # try lowercase variant
    if clean.lower() in translation_map:
        return translation_map[clean.lower()]

    # replace underscores with spaces and retry
    spaced = clean.replace("_", " ").strip()
    if spaced in translation_map:
        return translation_map[spaced]

    if spaced.lower() in translation_map:
        return translation_map[spaced.lower()]

    # strip accents and retry for terms like "Arándanos"
    import unicodedata
    normalized = unicodedata.normalize("NFD", clean)
    ascii_clean = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    if ascii_clean in translation_map:
        return translation_map[ascii_clean]
    if ascii_clean.lower() in translation_map:
        return translation_map[ascii_clean.lower()]

    # no match found, return cleaned term as-is
    return clean


if __name__ == "__main__":
    print("=" * 60)
    print("  task 2 — bilingual translation test")
    print("=" * 60)

    # test cases covering carlos spec examples and filename variants
    test_cases = [
        ("Certificado Fitosanitario",     "Phytosanitary Certificate"),
        ("Arándanos",                      "Blueberries"),
        ("Arandanos",                      "Blueberries"),
        ("certificado_fitosanitario.pdf", "Phytosanitary Certificate"),
        ("aviso_previo_fda.pdf",          "FDA Prior Notice"),
        ("registro_instalacion_fda.pdf",  "FDA Food Facility Registration"),
        ("factura_comercial.pdf",         "Commercial Invoice"),
        ("lista_de_empaque.pdf",          "Packing List"),
        ("Esparragos",                    "Asparagus"),
        ("Uvas",                          "Grapes"),
        ("Cafe Verde",                    "Coffee_Green"),
        ("Cafe Tostado",                  "Coffee_Roasted"),
        ("Quinua",                        "Quinoa"),
        ("Estados Unidos",                "USA"),
        ("unknown_document.pdf",          "unknown_document"),
    ]

    passed = 0
    failed = 0

    for term, expected in test_cases:
        result = translate_term(term)
        status = "PASS" if result == expected else "FAIL"
        passed += 1 if status == "PASS" else 0
        failed += 1 if status == "FAIL" else 0
        print(f"  {status}  '{term}' → '{result}'")

    print()
    print(f"  result: {passed} passed, {failed} failed")
    if failed == 0:
        print("  task 2 complete")
    print("=" * 60)