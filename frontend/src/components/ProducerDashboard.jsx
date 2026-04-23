import React, { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { CheckCircle2, AlertTriangle, FileText, Globe, CalendarDays, ShieldCheck, Upload } from "lucide-react";

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

export default function CultiveConnectProducerDashboard() {
  const [destination, setDestination] = useState("USA");
  const [product, setProduct] = useState("Grapes");
  const [shipmentDate, setShipmentDate] = useState("2026-03-19");
  const [filenameInput, setFilenameInput] = useState(
    "aviso_previo_fda.pdf, certificado_fitosanitario.pdf, factura_comercial.pdf, registro_instalacion_fda.pdf"
  );

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

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold tracking-tight">CultiveConnect Producer Dashboard</h1>
          <p className="text-slate-600">
            MVP interface for export document tracking, bilingual validation, and compliance gap analysis.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="rounded-2xl shadow-sm lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <Globe className="h-5 w-5" /> Shipment Input
              </CardTitle>
              <CardDescription>Choose product, destination, shipment date, and uploaded files.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Destination</Label>
                <Select
                  value={destination}
                  onValueChange={(value) => {
                    setDestination(value);
                    const nextProducts = Object.keys(regulations[value] || {});
                    setProduct(nextProducts[0] || "");
                  }}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select destination" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.keys(regulations).map((country) => (
                      <SelectItem key={country} value={country}>
                        {country}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Product</Label>
                <Select value={product} onValueChange={setProduct}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select product" />
                  </SelectTrigger>
                  <SelectContent>
                    {products.map((item) => (
                      <SelectItem key={item} value={item}>
                        {item}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Shipment Date</Label>
                <div className="relative">
                  <CalendarDays className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    className="pl-9"
                    type="date"
                    value={shipmentDate}
                    onChange={(e) => setShipmentDate(e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Uploaded Filenames</Label>
                <div className="relative">
                  <Upload className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    className="pl-9"
                    value={filenameInput}
                    onChange={(e) => setFilenameInput(e.target.value)}
                    placeholder="Separate filenames with commas"
                  />
                </div>
                <p className="text-xs text-slate-500">
                  Example: certificado_fitosanitario.pdf, aviso_previo_fda.pdf
                </p>
              </div>
            </CardContent>
          </Card>

          <div className="space-y-6 lg:col-span-2">
            <div className="grid gap-6 md:grid-cols-3">
              <Card className="rounded-2xl shadow-sm">
                <CardHeader className="pb-2">
                  <CardDescription>HTS / HS Code</CardDescription>
                  <CardTitle className="text-2xl">{analysis?.htsCode || "-"}</CardTitle>
                </CardHeader>
              </Card>

              <Card className="rounded-2xl shadow-sm">
                <CardHeader className="pb-2">
                  <CardDescription>Base Duty</CardDescription>
                  <CardTitle className="text-2xl">{analysis?.baseDuty || "-"}</CardTitle>
                </CardHeader>
              </Card>

              <Card className="rounded-2xl shadow-sm">
                <CardHeader className="pb-2">
                  <CardDescription>Status</CardDescription>
                  <div>
                    <Badge
                      variant={analysis?.status === "READY" ? "default" : "secondary"}
                      className="text-sm"
                    >
                      {analysis?.status || "-"}
                    </Badge>
                  </div>
                </CardHeader>
              </Card>
            </div>

            <Card className="rounded-2xl shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-xl">
                  <ShieldCheck className="h-5 w-5" /> Export Readiness
                </CardTitle>
                <CardDescription>Document coverage against required compliance items.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between text-sm text-slate-600">
                  <span>Coverage</span>
                  <span>{analysis?.percent || 0}%</span>
                </div>
                <Progress value={analysis?.percent || 0} />
              </CardContent>
            </Card>

            {analysis?.seasonal?.seasonalApplied ? (
              <Alert className="border-amber-300 bg-amber-50 rounded-2xl">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>Seasonal Alert</AlertTitle>
                <AlertDescription>
                  This shipment falls in the <strong>{analysis.seasonal.period}</strong> seasonal window. Use
                  subheading <strong>{analysis.seasonal.subheading}</strong> and review the applicable duty of{" "}
                  <strong>{analysis.seasonal.duty}</strong>.
                </AlertDescription>
              </Alert>
            ) : (
              <Alert className="border-emerald-300 bg-emerald-50 rounded-2xl">
                <CheckCircle2 className="h-4 w-4" />
                <AlertTitle>No seasonal tariff window triggered</AlertTitle>
                <AlertDescription>
                  The product follows the standard year-round classification for this shipment date.
                </AlertDescription>
              </Alert>
            )}

            <div className="grid gap-6 md:grid-cols-2">
              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Translated Uploads</CardTitle>
                  <CardDescription>Spanish filenames are mapped to compliance document names.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {analysis?.translatedUploads.map((item, index) => (
                    <div key={`${item.original}-${index}`} className="rounded-xl border p-3 text-sm">
                      <div className="font-medium">{item.original}</div>
                      <div className="text-slate-500">{item.translated}</div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Gap Analysis</CardTitle>
                  <CardDescription>Required documents minus provided documents.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="mb-2 flex items-center gap-2 font-medium text-emerald-700">
                      <CheckCircle2 className="h-4 w-4" /> Received Documents
                    </div>
                    <div className="space-y-2">
                      {analysis?.receivedDocs.length ? (
                        analysis.receivedDocs.map((doc) => (
                          <div
                            key={doc}
                            className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm"
                          >
                            {doc}
                          </div>
                        ))
                      ) : (
                        <div className="rounded-xl border p-3 text-sm text-slate-500">
                          No received documents matched yet.
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <div className="mb-2 flex items-center gap-2 font-medium text-rose-700">
                      <AlertTriangle className="h-4 w-4" /> Missing Documents
                    </div>
                    <div className="space-y-2">
                      {analysis?.missingDocs.length ? (
                        analysis.missingDocs.map((doc) => (
                          <div
                            key={doc}
                            className="rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm"
                          >
                            {doc}
                          </div>
                        ))
                      ) : (
                        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                          All required documents are present.
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="rounded-2xl shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-xl">
                  <FileText className="h-5 w-5" /> Producer-Friendly Summary
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-slate-700">
                <p>
                  Your shipment is going to <strong>{destination}</strong> with product <strong>{product}</strong>.
                </p>
                <p>
                  The system checked your uploaded filenames, translated any Spanish document names,
                  compared them against the required compliance documents, and reviewed the shipment date
                  for seasonal tariff rules.
                </p>
                <p>
                  <strong>Current result:</strong>{" "}
                  {analysis?.missingDocs.length
                    ? `You still need ${analysis.missingDocs.length} required document${
                        analysis.missingDocs.length > 1 ? "s" : ""
                      } before this shipment is ready.`
                    : "Your shipment currently has all required documents listed in the compliance engine."}
                </p>
              </CardContent>
            </Card>

            <div className="flex gap-3">
              <Button
                onClick={() => {
                  setDestination("USA");
                  setProduct("Grapes");
                  setShipmentDate("2026-03-19");
                  setFilenameInput(
                    "aviso_previo_fda.pdf, certificado_fitosanitario.pdf, factura_comercial.pdf, registro_instalacion_fda.pdf"
                  );
                }}
              >
                Load Grapes Demo
              </Button>

              <Button
                variant="outline"
                onClick={() => {
                  setDestination("Canada");
                  setProduct("Asparagus");
                  setShipmentDate("2026-06-20");
                  setFilenameInput("certificado_fitosanitario.pdf, factura_comercial.pdf");
                }}
              >
                Load Asparagus Demo
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}