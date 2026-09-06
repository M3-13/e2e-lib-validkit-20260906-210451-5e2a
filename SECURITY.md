VERDICT: CHANGES_REQUESTED

## Sicherheitsbericht

Die Scanner `bandit` und `semgrep` wurden nicht ausgeführt (`[skipped]`). Die nachfolgenden Befunde basieren daher ausschließlich auf manueller Analyse des sichtbaren Produktcodes. Es wurden keine hartkodierten Geheimnisse, keine Verwendung unsicherer Deserialisierung (`eval`, `exec`, `pickle`, `subprocess`) und keine externen Abhängigkeiten mit bekannten Schwachstellen festgestellt. Die Bibliothek arbeitet ausschließlich mit der Python-Standardbibliothek und hat keine Angriffsfläche durch Netzwerk, Authentifizierung oder Konfiguration.

Dennoch bestehen einige Härtungsbedarfe, insbesondere bei der IBAN-Prüfung und bei der strikten Eingabetypvalidierung.

---

### Findings

#### 1. Mittel – Unbegrenzte Eingabelänge in `is_valid_iban` kann zu unerwarteter `ValueError` führen

**Datei/Stelle:** `validkit/iban.py`, Zeile `return int(digits) % 97 == 1`

**Beschreibung:**  
`is_valid_iban` prüft nur, dass die normalisierte Eingabe mindestens fünf Zeichen lang ist. Eine extrem lange, aus ASCII-Buchstaben/-Ziffern bestehende IBAN (z. B. mehrere tausend Zeichen) wird durch die Validierung gelassen. Beim Aufruf von `int(digits)` überschreitet die erzeugte Ziffernfolge das Python-Limit für die Konvertierung von Zeichenketten in Ganzzahlen (`sys.set_int_max_str_digits`, standardmäßig 4300 Stellen). Dadurch wird eine unerwartete `ValueError` ausgelöst, obwohl die Funktion bei ungültiger Eingabe laut API `False` zurückgeben sollte. Dies kann in Anwendungen, die IBANs aus ungeprüften Nutzereingaben validieren, zu einem Denial-of-Service über Exceptions führen.

**Konkreter Fix:**  
Vor der Umwandlung eine maximale IBAN-Länge prüfen – IBANs sind nach Standard auf 34 Zeichen begrenzt:

```python
if len(normalized) > 34:
    return False
```

Alternativ kann die Modulo-97-Prüfung iterativ ohne große Ganzzahl durchgeführt werden, um das Limit vollständig zu vermeiden.

---

#### 2. Niedrig – E-Mail-Validator akzeptiert problematische Adressen

**Datei/Stelle:** `validkit/email.py`, Zeile `_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")`

**Beschreibung:**  
Die Regex ist bewusst einfach gehalten und erfüllt die grundlegenden Testfälle. Sie akzeptiert jedoch auch offensichtlich ungültige Adressen wie `a@b..co` oder `user@example..com`, weil der Teil vor dem Punkt auch Punkte enthalten darf. Wird diese Funktion als vorgelagerte Validierung für sicherheitsrelevante E-Mail-Flows (z. B. Registrierung, Benachrichtigungen) verwendet, kann dies zu Fehlakzeptanz führen. Eine unmittelbare Codeausführung ist nicht möglich; es handelt sich um eine Verbesserung der Eingabequalität.

**Konkreter Fix:**  
Strengere Regex verwenden, die Punkte im Domainteil korrekt behandelt, z. B.:

```python
_EMAIL_RE = re.compile(r"^[^@\s]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
```

Die genaue Regel sollte an die gewünschte E-Mail-Policy angepasst werden.

---

#### 3. Niedrig – `luhn_check` akzeptiert Unicode-Ziffern

**Datei/Stelle:** `validkit/luhn.py`, Zeile `if not digits.isdigit():`

**Beschreibung:**  
`str.isdigit()` liefert auch für Unicode-Ziffern (z. B. arabische Ziffern) `True`. Damit werden Zeichen akzeptiert, die nicht dem erwarteten Format von Kreditkartennummern entsprechen und in nachgelagerten Systemen zu Interpretationsunterschieden führen können (Homoglyph-Risiko). Die Anforderung AC-03 spricht von „Nicht-Ziffern“, wobei im Kontext einer Kreditkartenprüfung ASCII-Ziffern gemeint sind.

**Konkreter Fix:**  
ASCII-only-Prüfung erzwingen:

```python
if not digits.isascii() or not digits.isdigit():
    raise ValueError("luhn_check requires a string containing only ASCII digits")
```

---

#### 4. Niedrig – `mask_secret` akzeptiert `bool` für `keep`

**Datei/Stelle:** `validkit/secret.py`, Zeile `if not isinstance(keep, int):`

**Beschreibung:**  
Da `bool` eine Unterklasse von `int` ist, lässt die Typprüfung `keep=True` oder `keep=False` durch. Dadurch wird `True` als `1` interpretiert und es werden unerwartet viele Zeichen sichtbar. Die übrigen Funktionen (z. B. `clamp`) lehnen `bool` explizit ab; hier fehlt diese Konsistenz.

**Konkreter Fix:**  
Bool vor der Int-Prüfung ausschließen:

```python
if isinstance(keep, bool) or not isinstance(keep, int):
    raise TypeError("keep must be an int")
```

---

#### 5. Niedrig – Fehlermeldung in `normalize_phone` reflektiert Nutzereingabe

**Datei/Stelle:** `validkit/phone.py`, Zeile `raise ValueError(f"unknown country_code: {country_code}")`

**Beschreibung:**  
Die Fehlermeldung enthält den ungeprüften Wert des Parameters `country_code`. Falls die Meldung in Logs, UIs oder API-Antworten ungefiltert ausgegeben wird, kann dies zu unerwünschter Inhaltsreflexion oder Log-Injection führen. Zwar werden keine internen Dateipfade oder Stacktraces preisgegeben (AC-12), die Spiegelung von rohen Eingaben ist jedoch unnötig.

**Konkreter Fix:**  
Generische Fehlermeldung verwenden:

```python
raise ValueError("unknown country_code")
```

---

#### 6. Niedrig – IBAN-Prüfziffern akzeptieren Unicode-Ziffern

**Datei/Stelle:** `validkit/iban.py`, Zeile `if not check_digits.isdigit():`

**Beschreibung:**  
Wie bei `luhn_check` kann `check_digits.isdigit()` für Unicode-Ziffern `True` liefern. Die anschließende `int()`-Konvertierung akzeptiert einige Unicode-Ziffern, sodass eine formal ungültige IBAN unter Umständen als gültig gewertet wird. Für eine konsistente, standardkonforme Prüfung sollten ausschließlich ASCII-Ziffern zugelassen werden.

**Konkreter Fix:**  
Analog zu oben ergänzen:

```python
if not (check_digits.isascii() and check_digits.isdigit()):
    return False
```

---

### Zusammenfassung

- **Kritische oder hohe Schwachstellen:** keine.
- **Mittlere Härtungsmaßnahme:** Längenbegrenzung in der IBAN-Prüfung.
- **Niedrige Härtungsmaßnahmen:** striktere Typ-/Zeichenvalidierung und Vermeidung reflektierter Eingaben in Fehlermeldungen.
- **Scanner-Lücke:** `bandit` und `semgrep` wurden nicht ausgeführt; die manuelle Analyse deckt den sichtbaren Python-Code ab.