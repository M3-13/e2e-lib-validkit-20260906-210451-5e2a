VERDICT: CHANGES_REQUESTED

## Prüfbericht

**Projekt:** validkit – eigenständige Python-Bibliothek  
**Projekttyp:** `python-backend` (reine Bibliothek ohne Endnutzer-UI)  
**Prüfumfang:** Gesamtzustand des gemergten Produkts gemäß den sichtbaren Quelldateien, Tests und Spezifikation.  
**Verdikt:** `CHANGES_REQUESTED` – behebbare Lücken im Bereich CRA; keine datenschutzrechtlichen Blocker, keine KI-Pflichten, keine UI-/Barrierefreiheitspflichten.

---

## 1. GDPR (Datenschutz-Grundverordnung)

**Bewertung:** Keine offenen Verstöße. Die Bibliothek verarbeitet personenbezogene Daten nur als flüchtige Eingabewerte im Arbeitsspeicher des aufrufenden Prozesses. Es findet keine Speicherung, Protokollierung, Übermittlung an Dritte oder sonstige Verarbeitung mit eigener Entscheidungsgewalt statt. Die Bibliothek ist kein Verantwortlicher im Sinne des Art. 4 Nr. 7 DSGVO; die datenschutzrechtliche Verantwortung liegt beim jeweiligen Aufrufer, der die Bibliothek in seine Anwendung einbettet.

**Prüfpunkte:**

| Kriterium | Befund | Schwere | Konkrete Abhilfe |
|---|---|---|---|
| Verarbeitung personenbezogener Daten | Nur im flüchtigen Speicher; keine Persistenz, keine Logs, keine Netzwerkübertragung. | – (kein Befund) | Keine Maßnahme erforderlich. |
| Datenminimierung | Funktionen geben ausschließlich die für ihre Aufgabe notwendigen Ergebnisse zurück; keine Speicherung von Zusatzdaten. | – | Keine Maßnahme erforderlich. |
| Fehlermeldungen ohne interne Details | Alle TypeError-Meldungen sind kurz und enthalten keine Stacktraces, Dateipfade oder `.py`-Verweise. Einzige Rückgabe eines Eingabewerts: `normalize_phone` gibt bei unbekanntem Ländercode `country_code` im Fehlertext aus. Hierbei handelt es sich nicht um personenbezogene Daten im Sinne der DSGVO. | low | Sollte künftig vermieden werden, PII in Fehlertexte aufzunehmen. Aktuell unkritisch. |
| Datenübermittlung in Drittländer | Nicht vorhanden. | – | Keine Maßnahme erforderlich. |
| Auftragsverarbeitung | Nicht anwendbar; Bibliothek wird vom Aufrufer direkt eingebunden. | – | Keine Maßnahme erforderlich. |

**Hinweis:** Der Aufrufer der Bibliothek ist für eine rechtmäßige Verarbeitung der übergebenen Daten verantwortlich. Eine kurze Erwähnung in der README („Der Verwender muss die DSGVO-Konformität seiner Anwendung sicherstellen.“) wäre optional und nicht verpflichtend.

---

## 2. EU Cyber Resilience Act (CRA)

**Bewertung:** Grundlegende Security-by-Design-Anforderungen sind erfüllt. Es bestehen jedoch zwei behebbare Lücken bei der Dokumentation und Nachweisführung.

**Positiv:**

- Sämtliche öffentliche Funktionen validieren den Eingabetyp vor der Verarbeitung (`TypeError` bei falschem Typ).
- Keine Verwendung von `eval`, `exec`, `pickle`, `subprocess` oder ähnlichen unsicheren Mechanismen (AC-15 erfüllt).
- `slugify` liefert ausschließlich Zeichen aus `[a-z0-9-]`; Steuerzeichen und andere Unicode-Zeichen werden entfernt oder normalisiert (AC-13 erfüllt).
- `mask_secret` maskiert garantiert den gesamten Text, wenn die Länge kleiner oder gleich `keep` ist; der vollständige Klartext wird niemals zurückgegeben (AC-14 erfüllt).
- Keine Drittanbieter-Abhängigkeiten; ausschließlich Python-Standardbibliothek. Dadurch minimale Angriffsfläche und keine bekannten Supply-Chain-Risiken über externe Pakete.

**Befunde:**

| Kriterium | Befund | Schwere | Konkrete Abhilfe |
|---|---|---|---|
| SBOM (Software Bill of Materials) | Keine SBOM-Datei vorhanden (z. B. `sbom.spdx.json` oder `cyclonedx.json`). CRA verlangt für Produkte mit digitalen Elementen eine dokumentierte Stückliste der Komponenten. | medium | Datei `sbom.spdx.json` im Repository-Wurzelverzeichnis anlegen. Inhalt: SPDX-Dokument, `name: validkit`, `versionInfo: 0.1.0`, `packages`: nur die Bibliothek selbst, `externalRefs` leer, `relationships` – keine externen Abhängigkeiten. Alternativ mit einem Tool wie `syft` oder `cyclonedx-python` generieren. |
| Update- und Patch-Fähigkeit / dokumentierte Sicherheitseigenschaften | Keine `SECURITY.md` mit Kontaktadresse, Meldeweg für Sicherheitslücken oder dokumentiertem Prozess für Sicherheitsupdates. CRA verlangt, dass Hersteller Sicherheitsupdates bereitstellen und die Sicherheitseigenschaften dokumentieren. | medium | Datei `SECURITY.md` anlegen. Mindestinhalt: (1) Projektname und Version, (2) Kontakt für Sicherheitsmeldungen (z. B. E-Mail-Adresse), (3) Prozess für Sicherheitsupdates (z. B. „Sicherheitsrelevante Fehler werden innerhalb von X Tagen behoben und als Patch-Release veröffentlicht“), (4) Hinweis auf die verwendeten Sicherheitsmaßnahmen (Typvalidierung, keine unsicheren Sprachkonstrukte, keine Drittabhängigkeiten). |
| Sicherheitsdokumentation im Allgemeinen | README.md vorhanden, aber die sichtbaren 64 Zeilen wurden nicht vollständig geprüft; es ist unklar, ob dort Sicherheitsaspekte ausreichend dokumentiert sind. | low | README um einen kurzen Abschnitt „Sicherheit“ ergänzen, der die oben genannten Eigenschaften zusammenfasst. |

**Hinweis zur Reconcile-Regel:** Die geforderten Ergänzungen (SBOM, SECURITY.md) beeinträchtigen die Funktionsweise der Bibliothek nicht; sie sind rein deklarative Dateien.

---

## 3. EU AI Act

**Bewertung:** Nicht anwendbar. Das Produkt enthält keine KI-Funktion, kein maschinelles Lernen, kein generatives System und keine automatisierte Entscheidungsfindung. Keine weiteren Pflichten.

---

## 4. Pflichttexte & UI (Impressum, Datenschutzerklärung, Cookie-Banner, Widerrufsbelehrung)

**Bewertung:** Nicht anwendbar. Es handelt sich um eine reine Backend-Bibliothek ohne Endnutzer-UI, Webauftritt oder Verkaufsvorgang. Weder Impressum noch Datenschutzerklärung noch Cookie-Einwilligung sind für das Produkt selbst erforderlich. Die Verantwortung für etwaige UI-Pflichten liegt beim jeweiligen Anwendungsbetreiber, der die Bibliothek einbettet.

---

## 5. Barrierefreiheit (WCAG / BITV / EAA)

**Bewertung:** Nicht anwendbar. Keine öffentliche Web-UI, keine grafische Oberfläche, keine Interaktionselemente. Die Bibliothek stellt ausschließlich Python-Funktionen bereit.

---

## 6. Zusätzliche Beobachtungen zur Marktreife (außerhalb des regulierten Prüfumfangs)

Die folgenden Punkte sind **keine Verstöße gegen die genannten Regulierungen**, können jedoch die Marktreife und die rechtmäßige Distribution der Bibliothek behindern:

| Beobachtung | Schwere | Konkrete Abhilfe |
|---|---|---|
| Keine `LICENSE`-Datei vorhanden. Ohne Lizenz darf die Bibliothek nicht rechtssicher weitergegeben oder genutzt werden; dies ist urheberrechtlich relevant und für jede Distribution blockierend. | hoch (für Distribution) | Datei `LICENSE` anlegen und einen Standardtext (z. B. MIT- oder Apache-2.0-Lizenz) einfügen. Die Lizenzwahl sollte mit dem Projektverantwortlichen abgestimmt werden. |
| Keine `pyproject.toml` oder `setup.py` vorhanden. Dies erschwert Installation, Distribution und automatisierte SBOM-Generierung; eine Veröffentlichung auf PyPI ist derzeit nicht möglich. | medium | Datei `pyproject.toml` anlegen, z. B. mit `[project]`-Metadaten (Name, Version, dependencies = []), Build-Backend `setuptools` oder `hatchling`. |

Diese Punkte beeinflussen das Verdikt nicht, da sie nicht Gegenstand der vorgegebenen Regulierungsprüfung sind. Für eine erfolgreiche Markteinführung werden sie jedoch dringend empfohlen.

---

**Zusammenfassung:**  
Das Produkt ist aus datenschutzrechtlicher Sicht unbedenklich und erfüllt die grundlegenden CRA-Sicherheitsanforderungen. Für die volle CRA-Konformität und damit die Marktreife sind eine SBOM-Datei und eine `SECURITY.md` zu ergänzen. Die übrigen Bereiche (AI Act, Pflichttexte/UI, Barrierefreiheit) sind nicht einschlägig.