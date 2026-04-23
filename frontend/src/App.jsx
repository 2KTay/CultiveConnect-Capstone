import React, { useMemo, useState } from "react";
import livingStonesLogo from "./assets/living-stones-logo.png";

const translations = {
  en: {
    foundation: "Living Stones Foundation",
    title: "CultiveConnect Producer Dashboard",
    subtitle: "MVP for export document tracking, bilingual validation, and compliance gap analysis.",
    author: "Author: Taemoor Hasan",
    shipmentInput: "Shipment Input",
    shipmentInputDesc: "Choose destination, product, shipment date, and uploaded files.",
    destination: "Destination",
    product: "Product",
    shipmentDate: "Shipment Date",
    uploadedFilenames: "Uploaded Filenames",
    uploadedExample: "Example: certificado_fitosanitario.pdf, aviso_previo_fda.pdf",
    htsHsCode: "HTS / HS Code",
    baseDuty: "Base Duty",
    status: "Status",
    exportReadiness: "Export Readiness",
    exportReadinessDesc: "Document coverage against required compliance items.",
    coverage: "Coverage",
    seasonalAlert: "Seasonal Alert",
    noSeasonalAlert: "No Seasonal Tariff Window Triggered",
    noSeasonalDesc: "The product follows the standard year-round classification for this shipment date.",
    translatedUploads: "Translated Uploads",
    translatedUploadsDesc: "Spanish filenames are mapped to compliance document names.",
    gapAnalysis: "Gap Analysis",
    gapAnalysisDesc: "Required documents minus provided documents.",
    receivedDocuments: "Received Documents",
    missingDocuments: "Missing Documents",
    noReceivedDocs: "No received documents matched yet.",
    allDocsPresent: "All required documents are present.",
    producerSummary: "Producer-Friendly Summary",
    summary1Prefix: "Your shipment is going to",
    summary1Middle: "with product",
    summary2:
      "The system checked your uploaded filenames, translated any Spanish document names, compared them against the required compliance documents, and reviewed the shipment date for seasonal tariff rules.",
    currentResult: "Current result:",
    summaryReady: "Your shipment currently has all required documents listed in the compliance engine.",
    stillNeedPrefix: "You still need",
    stillNeedMiddle: "required document",
    stillNeedSuffix: "before this shipment is ready.",
    loadGrapes: "Load Grapes Demo",
    loadAsparagus: "Load Asparagus Demo",
    useSubheadingPrefix: "This shipment falls in the",
    useSubheadingMiddle: "seasonal window. Use subheading",
    useSubheadingSuffix: "and review the applicable duty of",
    language: "Language",
    ready: "READY",
    actionRequired: "ACTION REQUIRED",
    criticalGaps: "CRITICAL GAPS",
  },
  es: {
    foundation: "Living Stones Foundation",
    title: "Panel del Productor de CultiveConnect",
    subtitle: "MVP para seguimiento de documentos de exportación, validación bilingüe y análisis de brechas de cumplimiento.",
    author: "Autor: Taemoor Hasan",
    shipmentInput: "Entrada del Envío",
    shipmentInputDesc: "Elige destino, producto, fecha de envío y archivos cargados.",
    destination: "Destino",
    product: "Producto",
    shipmentDate: "Fecha de Envío",
    uploadedFilenames: "Nombres de Archivos Cargados",
    uploadedExample: "Ejemplo: certificado_fitosanitario.pdf, aviso_previo_fda.pdf",
    htsHsCode: "Código HTS / HS",
    baseDuty: "Arancel Base",
    status: "Estado",
    exportReadiness: "Preparación para Exportación",
    exportReadinessDesc: "Cobertura documental frente a los requisitos de cumplimiento.",
    coverage: "Cobertura",
    seasonalAlert: "Alerta Estacional",
    noSeasonalAlert: "No se Activó Ventana Arancelaria Estacional",
    noSeasonalDesc: "El producto sigue la clasificación estándar de todo el año para esta fecha de envío.",
    translatedUploads: "Archivos Traducidos",
    translatedUploadsDesc: "Los nombres de archivos en español se convierten a nombres de documentos de cumplimiento.",
    gapAnalysis: "Análisis de Brechas",
    gapAnalysisDesc: "Documentos requeridos menos documentos proporcionados.",
    receivedDocuments: "Documentos Recibidos",
    missingDocuments: "Documentos Faltantes",
    noReceivedDocs: "Todavía no hay documentos recibidos que coincidan.",
    allDocsPresent: "Todos los documentos requeridos están presentes.",
    producerSummary: "Resumen para el Productor",
    summary1Prefix: "Tu envío va a",
    summary1Middle: "con el producto",
    summary2:
      "El sistema revisó los nombres de tus archivos cargados, tradujo los nombres de documentos en español, los comparó con los documentos requeridos de cumplimiento y revisó la fecha de envío para reglas arancelarias estacionales.",
    currentResult: "Resultado actual:",
    summaryReady: "Tu envío actualmente tiene todos los documentos requeridos listados en el motor de cumplimiento.",
    stillNeedPrefix: "Todavía necesitas",
    stillNeedMiddle: "documento requerido",
    stillNeedSuffix: "antes de que este envío esté listo.",
    loadGrapes: "Cargar Demo de Uvas",
    loadAsparagus: "Cargar Demo de Espárragos",
    useSubheadingPrefix: "Este envío cae en la ventana estacional de",
    useSubheadingMiddle: ". Usa la subpartida",
    useSubheadingSuffix: "y revisa el arancel aplicable de",
    language: "Idioma",
    ready: "LISTO",
    actionRequired: "ACCIÓN REQUERIDA",
    criticalGaps: "BRECHAS CRÍTICAS",
  },
  pt: {
    foundation: "Living Stones Foundation",
    title: "Painel do Produtor CultiveConnect",
    subtitle: "MVP para rastreamento de documentos de exportação, validação bilíngue e análise de lacunas de conformidade.",
    author: "Autor: Taemoor Hasan",
    shipmentInput: "Entrada do Envio",
    shipmentInputDesc: "Escolha destino, produto, data de envio e arquivos enviados.",
    destination: "Destino",
    product: "Produto",
    shipmentDate: "Data do Envio",
    uploadedFilenames: "Nomes dos Arquivos Enviados",
    uploadedExample: "Exemplo: certificado_fitosanitario.pdf, aviso_previo_fda.pdf",
    htsHsCode: "Código HTS / HS",
    baseDuty: "Tarifa Base",
    status: "Status",
    exportReadiness: "Prontidão para Exportação",
    exportReadinessDesc: "Cobertura documental em relação aos itens exigidos de conformidade.",
    coverage: "Cobertura",
    seasonalAlert: "Alerta Sazonal",
    noSeasonalAlert: "Nenhuma Janela Tarifária Sazonal Acionada",
    noSeasonalDesc: "O produto segue a classificação padrão durante todo o ano para esta data de envio.",
    translatedUploads: "Uploads Traduzidos",
    translatedUploadsDesc: "Nomes de arquivos em espanhol são mapeados para nomes de documentos de conformidade.",
    gapAnalysis: "Análise de Lacunas",
    gapAnalysisDesc: "Documentos exigidos menos documentos fornecidos.",
    receivedDocuments: "Documentos Recebidos",
    missingDocuments: "Documentos Faltando",
    noReceivedDocs: "Ainda não há documentos recebidos correspondentes.",
    allDocsPresent: "Todos os documentos exigidos estão presentes.",
    producerSummary: "Resumo para o Produtor",
    summary1Prefix: "Seu envio vai para",
    summary1Middle: "com o produto",
    summary2:
      "O sistema verificou os nomes dos arquivos enviados, traduziu nomes de documentos em espanhol, comparou com os documentos exigidos de conformidade e revisou a data de envio para regras tarifárias sazonais.",
    currentResult: "Resultado atual:",
    summaryReady: "Seu envio atualmente possui todos os documentos exigidos listados no mecanismo de conformidade.",
    stillNeedPrefix: "Você ainda precisa de",
    stillNeedMiddle: "documento exigido",
    stillNeedSuffix: "antes que este envio esteja pronto.",
    loadGrapes: "Carregar Demo de Uvas",
    loadAsparagus: "Carregar Demo de Aspargos",
    useSubheadingPrefix: "Este envio cai na janela sazonal de",
    useSubheadingMiddle: ". Use a subposição",
    useSubheadingSuffix: "e revise a tarifa aplicável de",
    language: "Idioma",
    ready: "PRONTO",
    actionRequired: "AÇÃO NECESSÁRIA",
    criticalGaps: "LACUNAS CRÍTICAS",
  },
};

const regulations = {
  USA: {
    Blueberries: {
      hts_code: "0810.40.00",
      base_duty: "Free",
      required_docs: [
        "Phytosanitary Certificate",
        "Port of Entry Inspection",
        "FDA Prior Notice",
        "FDA Food Facility Registration",
      ],
      seasonal_adjustment: { applies: false, note: "No seasonal tariff windows." },
    },
    Grapes: {
      hts_code: "0806.10",
      base_duty: "Free",
      required_docs: [
        "Phytosanitary Certificate",
        "Port of Entry Inspection",
        "FDA Prior Notice",
        "FDA Food Facility Registration",
      ],
      seasonal_adjustment: {
        applies: true,
        windows: [
          { period: "February 1 to July 31", subheading: "0806.10.20", duty: "Free" },
          { period: "August 1 to January 31", subheading: "0806.10.40", duty: "Free" },
        ],
      },
    },
    Coffee_Green: {
      hts_code: "0901.11",
      base_duty: "Free",
      required_docs: ["FDA Prior Notice", "FDA Food Facility Registration"],
      seasonal_adjustment: { applies: false, note: "Year-round classification." },
    },
    Quinoa: {
      hts_code: "1008.50.00.10",
      base_duty: "1.1% ad valorem",
      required_docs: ["FDA Prior Notice", "FDA Food Facility Registration"],
      seasonal_adjustment: { applies: false, note: "Year-round classification." },
    },
  },
  Canada: {
    Asparagus: {
      hs_code: "0709.20",
      base_duty: "Free (MFN)",
      required_docs: [
        "Phytosanitary Certificate",
        "AIRS Verification",
        "Port of Entry Inspection",
      ],
      seasonal_adjustment: {
        applies: true,
        windows: [
          { period: "October 1 to June 14", subheading: "0709.20.10", duty: "Free" },
          { period: "June 15 to September 30", subheading: "0709.20.90", duty: "Free" },
        ],
      },
    },
  },
};

const productLabels = {
  Blueberries: { en: "Blueberries", es: "Arándanos", pt: "Mirtilos" },
  Grapes: { en: "Grapes", es: "Uvas", pt: "Uvas" },
  Coffee_Green: { en: "Green Coffee", es: "Café Verde", pt: "Café Verde" },
  Quinoa: { en: "Quinoa", es: "Quinua", pt: "Quinoa" },
  Asparagus: { en: "Asparagus", es: "Espárragos", pt: "Aspargos" },
};

const countryLabels = {
  USA: { en: "USA", es: "EE. UU.", pt: "EUA" },
  Canada: { en: "Canada", es: "Canadá", pt: "Canadá" },
};

const translationMap = {
  certificado_fitosanitario: "Phytosanitary Certificate",
  aviso_previo_fda: "FDA Prior Notice",
  registro_instalacion_fda: "FDA Food Facility Registration",
  verificacion_airs: "AIRS Verification",
  verificacion_cfia: "AIRS Verification",
  inspeccion_puerto_entrada: "Port of Entry Inspection",
  inspeccion_portuaria: "Port of Entry Inspection",
  factura_comercial: "Commercial Invoice",
  lista_de_empaque: "Packing List",
  conocimiento_de_embarque: "Bill of Lading",
  commercial_invoice: "Commercial Invoice",
  bill_of_lading: "Bill of Lading",
  phytosanitary_certificate: "Phytosanitary Certificate",
  fda_prior_notice: "FDA Prior Notice",
  fda_food_facility_registration: "FDA Food Facility Registration",
};

function translateFilename(filename) {
  const clean = filename.replace(/\.pdf$/i, "").trim().toLowerCase();
  return translationMap[clean] || clean.replace(/_/g, " ");
}

function parseMonthDay(text, year) {
  return new Date(`${text}, ${year}`);
}

function getSeasonalResult(productData, shipmentDate) {
  const seasonal = productData?.seasonal_adjustment;

  if (!seasonal?.applies || !seasonal.windows?.length) {
    return {
      seasonalApplied: false,
      period: "Year-round",
      duty: productData?.base_duty || "See regulations",
      subheading: productData?.hts_code || productData?.hs_code || "",
    };
  }

  const year = shipmentDate.getFullYear();

  for (const window of seasonal.windows) {
    const [startLabel, endLabel] = window.period.split(" to ");
    const start = parseMonthDay(startLabel, year);
    const end = parseMonthDay(endLabel, year);

    let inWindow = false;
    if (start <= end) {
      inWindow = shipmentDate >= start && shipmentDate <= end;
    } else {
      inWindow = shipmentDate >= start || shipmentDate <= end;
    }

    if (inWindow) {
      return {
        seasonalApplied: true,
        period: window.period,
        duty: window.duty,
        subheading: window.subheading,
      };
    }
  }

  return {
    seasonalApplied: false,
    period: "Outside defined windows",
    duty: productData?.base_duty || "See regulations",
    subheading: productData?.hts_code || productData?.hs_code || "",
  };
}

function badgeColor(status) {
  if (status === "READY") return "#16a34a";
  if (status === "ACTION REQUIRED") return "#d97706";
  return "#dc2626";
}

function cardStyle() {
  return {
    background: "rgba(255,255,255,0.045)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "22px",
    padding: "22px",
    boxShadow: "0 8px 30px rgba(0,0,0,0.35)",
    backdropFilter: "blur(10px)",
  };
}

function inputStyle() {
  return {
    width: "100%",
    padding: "12px 13px",
    borderRadius: "14px",
    border: "1px solid rgba(255,255,255,0.12)",
    background: "#0b1220",
    color: "#f8fafc",
    outline: "none",
    boxSizing: "border-box",
    fontSize: "15px",
  };
}

export default function App() {
  const [language, setLanguage] = useState("en");
  const [destination, setDestination] = useState("USA");
  const [product, setProduct] = useState("Grapes");
  const [shipmentDate, setShipmentDate] = useState("2026-03-19");
  const [filenameInput, setFilenameInput] = useState(
    "aviso_previo_fda.pdf, certificado_fitosanitario.pdf, factura_comercial.pdf, registro_instalacion_fda.pdf"
  );

  const t = translations[language];
  const products = useMemo(() => Object.keys(regulations[destination] || {}), [destination]);
  const currentProductData = regulations[destination]?.[product];

  const analysis = useMemo(() => {
    if (!currentProductData) return null;

    const uploadedFiles = filenameInput
      .replace(/\n/g, ",")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    const translatedUploads = uploadedFiles.map((file) => ({
      original: file,
      translated: translateFilename(file),
    }));

    const normalizedUploads = translatedUploads.map((f) => f.translated.toLowerCase().trim());
    const requiredDocs = currentProductData.required_docs || [];

    const receivedDocs = [];
    const missingDocs = [];

    for (const doc of requiredDocs) {
      const target = doc.toLowerCase().trim();
      const matched = normalizedUploads.some(
        (name) => target === name || name.includes(target) || target.includes(name)
      );

      if (matched) {
        receivedDocs.push(doc);
      } else {
        missingDocs.push(doc);
      }
    }

    const dateObj = new Date(`${shipmentDate}T00:00:00`);
    const seasonal = getSeasonalResult(currentProductData, dateObj);
    const percent = requiredDocs.length
      ? Math.round((receivedDocs.length / requiredDocs.length) * 100)
      : 0;

    const status =
      missingDocs.length === 0
        ? "READY"
        : missingDocs.length <= 2
        ? "ACTION REQUIRED"
        : "CRITICAL GAPS";

    return {
      uploadedFiles,
      translatedUploads,
      requiredDocs,
      receivedDocs,
      missingDocs,
      seasonal,
      percent,
      status,
      htsCode: currentProductData.hts_code || currentProductData.hs_code,
      baseDuty: currentProductData.base_duty,
    };
  }, [currentProductData, filenameInput, shipmentDate]);

  const localizedStatus =
    analysis?.status === "READY"
      ? t.ready
      : analysis?.status === "ACTION REQUIRED"
      ? t.actionRequired
      : t.criticalGaps;

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "#000000",
        padding: "20px 24px",
        fontFamily: "Inter, Arial, sans-serif",
        color: "#f8fafc",
      }}
    >
      <div style={{ width: "100%", maxWidth: "1600px", margin: "0 auto" }}>
        <div
          style={{
            ...cardStyle(),
            marginBottom: "24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "20px",
            flexWrap: "wrap",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "18px", flexWrap: "wrap" }}>
            <img
              src={livingStonesLogo}
              alt="Living Stones Foundation logo"
              style={{
                width: "255px",
                maxWidth: "100%",
                borderRadius: "14px",
                objectFit: "contain",
              }}
            />
            <div>
              <h1
                style={{
                  margin: 0,
                  fontSize: "42px",
                  letterSpacing: "-0.8px",
                  fontFamily: "'Space Grotesk', 'Inter', Arial, sans-serif",
                  fontWeight: 700,
                }}
              >
                {t.title}
              </h1>
              <p style={{ margin: "8px 0 0 0", color: "#cbd5e1", fontSize: "17px" }}>
                {t.subtitle}
              </p>
              <p style={{ margin: "8px 0 0 0", color: "#94a3b8", fontSize: "14px" }}>
                {t.author}
              </p>
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "12px", minWidth: "170px" }}>
            <div
              style={{
                padding: "10px 16px",
                borderRadius: "999px",
                border: "1px solid rgba(255,255,255,0.12)",
                background: "rgba(255,255,255,0.04)",
                color: "#93c5fd",
                fontWeight: 600,
                textAlign: "center",
              }}
            >
              {t.foundation}
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "6px", color: "#94a3b8", fontSize: "13px" }}>
                {t.language}
              </label>
              <select value={language} onChange={(e) => setLanguage(e.target.value)} style={inputStyle()}>
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="pt">Português</option>
              </select>
            </div>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "380px minmax(0, 1fr)",
            gap: "24px",
            alignItems: "start",
            width: "100%",
          }}
        >
          <div style={cardStyle()}>
            <h2 style={{ marginTop: 0, marginBottom: "6px", fontSize: "24px" }}>{t.shipmentInput}</h2>
            <p style={{ color: "#94a3b8", marginTop: 0, marginBottom: "22px", lineHeight: 1.6 }}>
              {t.shipmentInputDesc}
            </p>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 700 }}>{t.destination}</label>
              <select
                value={destination}
                onChange={(e) => {
                  const value = e.target.value;
                  setDestination(value);
                  const nextProducts = Object.keys(regulations[value] || {});
                  setProduct(nextProducts[0] || "");
                }}
                style={inputStyle()}
              >
                {Object.keys(regulations).map((country) => (
                  <option key={country} value={country}>
                    {countryLabels[country]?.[language] || country}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 700 }}>{t.product}</label>
              <select value={product} onChange={(e) => setProduct(e.target.value)} style={inputStyle()}>
                {products.map((item) => (
                  <option key={item} value={item}>
                    {productLabels[item]?.[language] || item}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 700 }}>{t.shipmentDate}</label>
              <input
                type="date"
                value={shipmentDate}
                onChange={(e) => setShipmentDate(e.target.value)}
                style={inputStyle()}
              />
            </div>

            <div style={{ marginBottom: "14px" }}>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 700 }}>
                {t.uploadedFilenames}
              </label>
              <textarea
                value={filenameInput}
                onChange={(e) => setFilenameInput(e.target.value)}
                rows={7}
                placeholder="Separate filenames with commas"
                style={{
                  ...inputStyle(),
                  resize: "vertical",
                  minHeight: "150px",
                }}
              />
              <p style={{ color: "#94a3b8", fontSize: "12px", marginTop: "8px", lineHeight: 1.5 }}>
                {t.uploadedExample}
              </p>
            </div>
          </div>

          <div style={{ display: "grid", gap: "24px" }}>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)",
                gap: "16px",
              }}
            >
              <div style={cardStyle()}>
                <div style={{ color: "#94a3b8", marginBottom: "8px" }}>{t.htsHsCode}</div>
                <div style={{ fontSize: "32px", fontWeight: 800 }}>{analysis?.htsCode || "-"}</div>
              </div>

              <div style={cardStyle()}>
                <div style={{ color: "#94a3b8", marginBottom: "8px" }}>{t.baseDuty}</div>
                <div style={{ fontSize: "32px", fontWeight: 800 }}>{analysis?.baseDuty || "-"}</div>
              </div>

              <div style={cardStyle()}>
                <div style={{ color: "#94a3b8", marginBottom: "8px" }}>{t.status}</div>
                <span
                  style={{
                    display: "inline-block",
                    padding: "10px 14px",
                    borderRadius: "999px",
                    background: badgeColor(analysis?.status),
                    color: "#fff",
                    fontWeight: 800,
                    letterSpacing: "0.3px",
                    fontSize: "13px",
                  }}
                >
                  {localizedStatus}
                </span>
              </div>
            </div>

            <div style={cardStyle()}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "10px",
                }}
              >
                <div>
                  <h2 style={{ margin: 0, fontSize: "24px" }}>{t.exportReadiness}</h2>
                  <p style={{ margin: "6px 0 0 0", color: "#94a3b8" }}>
                    {t.exportReadinessDesc}
                  </p>
                </div>
                <div style={{ fontWeight: 700, fontSize: "18px" }}>{analysis?.percent || 0}%</div>
              </div>

              <div
                style={{
                  width: "100%",
                  height: "14px",
                  background: "#1e293b",
                  borderRadius: "999px",
                  overflow: "hidden",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                <div
                  style={{
                    width: `${analysis?.percent || 0}%`,
                    height: "100%",
                    background: "linear-gradient(90deg, #2563eb, #60a5fa)",
                  }}
                />
              </div>
            </div>

            <div
              style={{
                ...cardStyle(),
                background: analysis?.seasonal?.seasonalApplied
                  ? "rgba(245, 158, 11, 0.12)"
                  : "rgba(34, 197, 94, 0.10)",
                borderColor: analysis?.seasonal?.seasonalApplied
                  ? "rgba(245, 158, 11, 0.35)"
                  : "rgba(34, 197, 94, 0.28)",
              }}
            >
              {analysis?.seasonal?.seasonalApplied ? (
                <>
                  <h3 style={{ marginTop: 0, color: "#fbbf24", fontSize: "20px" }}>{t.seasonalAlert}</h3>
                  <p style={{ marginBottom: 0, color: "#f8fafc", lineHeight: 1.7, fontSize: "17px" }}>
                    {t.useSubheadingPrefix} <strong>{analysis.seasonal.period}</strong> {t.useSubheadingMiddle}{" "}
                    <strong>{analysis.seasonal.subheading}</strong> {t.useSubheadingSuffix}{" "}
                    <strong>{analysis.seasonal.duty}</strong>.
                  </p>
                </>
              ) : (
                <>
                  <h3 style={{ marginTop: 0, color: "#4ade80", fontSize: "20px" }}>{t.noSeasonalAlert}</h3>
                  <p style={{ marginBottom: 0, color: "#f8fafc", lineHeight: 1.7, fontSize: "17px" }}>
                    {t.noSeasonalDesc}
                  </p>
                </>
              )}
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "24px",
              }}
            >
              <div style={cardStyle()}>
                <h2 style={{ marginTop: 0, fontSize: "24px" }}>{t.translatedUploads}</h2>
                <p style={{ color: "#94a3b8" }}>{t.translatedUploadsDesc}</p>

                <div style={{ display: "grid", gap: "12px" }}>
                  {analysis?.translatedUploads.map((item, index) => (
                    <div
                      key={`${item.original}-${index}`}
                      style={{
                        border: "1px solid rgba(255,255,255,0.08)",
                        background: "rgba(255,255,255,0.03)",
                        borderRadius: "14px",
                        padding: "14px",
                      }}
                    >
                      <div style={{ fontWeight: 700 }}>{item.original}</div>
                      <div style={{ color: "#93c5fd", marginTop: "4px" }}>{item.translated}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div style={cardStyle()}>
                <h2 style={{ marginTop: 0, fontSize: "24px" }}>{t.gapAnalysis}</h2>
                <p style={{ color: "#94a3b8" }}>{t.gapAnalysisDesc}</p>

                <div style={{ marginBottom: "22px" }}>
                  <div style={{ fontWeight: 800, color: "#4ade80", marginBottom: "10px" }}>
                    {t.receivedDocuments}
                  </div>
                  <div style={{ display: "grid", gap: "10px" }}>
                    {analysis?.receivedDocs.length ? (
                      analysis.receivedDocs.map((doc) => (
                        <div
                          key={doc}
                          style={{
                            border: "1px solid rgba(74, 222, 128, 0.35)",
                            background: "rgba(34, 197, 94, 0.12)",
                            borderRadius: "12px",
                            padding: "12px",
                          }}
                        >
                          {doc}
                        </div>
                      ))
                    ) : (
                      <div
                        style={{
                          border: "1px solid rgba(255,255,255,0.08)",
                          background: "rgba(255,255,255,0.03)",
                          borderRadius: "12px",
                          padding: "12px",
                          color: "#94a3b8",
                        }}
                      >
                        {t.noReceivedDocs}
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <div style={{ fontWeight: 800, color: "#f87171", marginBottom: "10px" }}>
                    {t.missingDocuments}
                  </div>
                  <div style={{ display: "grid", gap: "10px" }}>
                    {analysis?.missingDocs.length ? (
                      analysis.missingDocs.map((doc) => (
                        <div
                          key={doc}
                          style={{
                            border: "1px solid rgba(248, 113, 113, 0.35)",
                            background: "rgba(239, 68, 68, 0.10)",
                            borderRadius: "12px",
                            padding: "12px",
                          }}
                        >
                          {doc}
                        </div>
                      ))
                    ) : (
                      <div
                        style={{
                          border: "1px solid rgba(74, 222, 128, 0.35)",
                          background: "rgba(34, 197, 94, 0.12)",
                          borderRadius: "12px",
                          padding: "12px",
                          color: "#4ade80",
                          fontWeight: 600,
                        }}
                      >
                        {t.allDocsPresent}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div style={cardStyle()}>
              <h2 style={{ marginTop: 0, fontSize: "24px" }}>{t.producerSummary}</h2>
              <p style={{ color: "#e2e8f0", lineHeight: 1.7 }}>
                {t.summary1Prefix} <strong>{countryLabels[destination]?.[language] || destination}</strong> {t.summary1Middle}{" "}
                <strong>{productLabels[product]?.[language] || product}</strong>.
              </p>
              <p style={{ color: "#cbd5e1", lineHeight: 1.7 }}>
                {t.summary2}
              </p>
              <p style={{ color: "#f8fafc", lineHeight: 1.7 }}>
                <strong>{t.currentResult}</strong>{" "}
                {analysis?.missingDocs.length
                  ? `${t.stillNeedPrefix} ${analysis.missingDocs.length} ${t.stillNeedMiddle}${
                      analysis.missingDocs.length > 1 ? "s" : ""
                    } ${t.stillNeedSuffix}`
                  : t.summaryReady}
              </p>
            </div>

            <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
              <button
                onClick={() => {
                  setDestination("USA");
                  setProduct("Grapes");
                  setShipmentDate("2026-03-19");
                  setFilenameInput(
                    "aviso_previo_fda.pdf, certificado_fitosanitario.pdf, factura_comercial.pdf, registro_instalacion_fda.pdf"
                  );
                }}
                style={{
                  padding: "12px 18px",
                  borderRadius: "12px",
                  border: "none",
                  background: "linear-gradient(90deg, #2563eb, #1d4ed8)",
                  color: "#fff",
                  cursor: "pointer",
                  fontWeight: 700,
                  boxShadow: "0 8px 20px rgba(37,99,235,0.35)",
                }}
              >
                {t.loadGrapes}
              </button>

              <button
                onClick={() => {
                  setDestination("Canada");
                  setProduct("Asparagus");
                  setShipmentDate("2026-06-20");
                  setFilenameInput("certificado_fitosanitario.pdf, factura_comercial.pdf");
                }}
                style={{
                  padding: "12px 18px",
                  borderRadius: "12px",
                  border: "1px solid rgba(255,255,255,0.12)",
                  background: "rgba(255,255,255,0.04)",
                  color: "#f8fafc",
                  cursor: "pointer",
                  fontWeight: 700,
                }}
              >
                {t.loadAsparagus}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}