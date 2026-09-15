---
name: ptw-friction-report
description: Rendert den Endstand eines /PTW-friction-Laufs (PTW-draft-final.md) als eigenständige, gut lesbare HTML-Übersicht — Choice-Cascade, Collision Log und gerankte Assumption-Map in einem Dokument, im überproduct Design-System.
when_to_use: Wenn der Nutzer /ptw-friction-report eingibt — nach einem /PTW-friction-Lauf, um den finalen Draft als durchgestyltes HTML statt als rohes Markdown zu lesen, zu drucken oder weiterzugeben.
---

# Skill: /ptw-friction-report

Liest `PTW-draft-final.md` aus einem `/PTW-friction`-Lauf und rendert ihn als standalone HTML-Datei. Keine Zusammenfassung, keine Bewertung — nur Formatierung. Quadrant B und der Collision Log sind laut PTW-friction selbst "der eigentliche Output"; diese Skill darf daraus nichts weglassen.

Diese Skill ist self-contained: die komplette Optik liegt in `template.html` direkt in diesem Ordner. Kein Zugriff auf ein externes Design-System nötig.

## Ablauf

### 1. Lauf finden

Falls ein Pfad als Argument übergeben wurde: den nehmen (darf auf `PTW-draft-final.md` selbst oder auf den Run-Ordner zeigen).

Sonst suchen unter `./PTW-friction/output/*/7_final/PTW-draft-final.md` (relativ zum aktiven Arbeitsverzeichnis):
- Kein Treffer → Nutzer informieren, dass zuerst `/PTW-friction` durchlaufen werden muss. Nicht raten, keinen leeren Report bauen.
- Genau ein Treffer → nehmen.
- Mehrere Treffer → Läufe mit Ordnername + Datum auflisten, Nutzer fragen welcher (Default-Vorschlag: der neueste nach Datum im Ordnernamen bzw. Datei-mtime).

### 2. Quelle lesen

`PTW-draft-final.md` vollständig lesen. Falls vorhanden, ergänzend `0_case/shared-brief.md` im selben Run nur zur Namensfindung überfliegen (nicht für den Report-Inhalt selbst — der Report bildet ausschließlich den finalen Draft ab).

### 3. Titel, Kunde, Datum ermitteln

- **Kunde**: aus dem Run-Ordnernamen ableiten (`run-<slug>-<datum>` → `<slug>`, Bindestriche zu Leerzeichen/Großschreibung), sonst aus der ersten konkreten Firmen-/Kundennennung im Draft (z. B. TL;DR oder Winning Aspiration). Kein Treffer → "PTW-Friction-Report".
- **Datum**: Datum im Ordnernamen, sonst Datei-mtime von `PTW-draft-final.md`, Format `DD.MM.YYYY`.
- **Titel**: die H1-Überschrift (`# ...`) am Kopf von `PTW-draft-final.md`, verbatim übernehmen (z. B. "PTW Choice Cascade — Final Synthesis (Friction Run)"). Keine eigene Überschrift erfinden.

### 4. Markdown-Struktur auf das Template abbilden

`template.html` in diesem Ordner öffnen (nicht verändern — eine Kopie mit ersetzten Platzhaltern schreiben). Platzhalter:

| Platzhalter | Inhalt |
|---|---|
| `<!--TITLE-->` | Titel aus Schritt 3 |
| `<!--CLIENT-->` | Kunde aus Schritt 3 |
| `<!--DATE-->` | Datum aus Schritt 3 |
| `<!--TLDR-->` | Text des TL;DR-Abschnitts, ohne Überschrift |
| `<!--TOC-->` | Ein `<a href="#sec-NN">NN · Titel</a>` pro Hauptabschnitt (H2), in Reihenfolge |
| `<!--BODY-->` | Alle Abschnitte außer TL;DR (das steht schon in der Lede), transformiert nach den Regeln unten |

**Pro Hauptabschnitt** (jedes `##` im Draft, außer TL;DR):
```html
<section class="report-section" id="sec-NN">
  <div class="eyebrow"><span class="num">§ NN</span><span>Kurzlabel</span><span class="rule"></span></div>
  <h2>Abschnittstitel</h2>
  ... transformierter Inhalt ...
</section>
```
NN = laufende Nummer (01, 02, …) in Dokumentreihenfolge. Kurzlabel = 1–2 Wörter Kategorie (z. B. "Choice 1", "Reverse Engineering").

**Inhalts-Transformation** (Formatierung, kein Umschreiben):
- `###`/`####` → `<h3>`/`<h4>`, Hierarchie erhalten.
- Aufzählungen → `<ul>`, nummerierte Listen → `<ol>` (Template stylt beide fertig).
- Markdown-Tabellen → `<table>` (z. B. die eingebettete `assumptions-ranked.md`-Tabelle, das Can't/Won't-Capabilities-Table).
- `**fett**` → `<strong>`, `*kursiv*`/`_kursiv_` → `<em>`.
- **Collision Log**: jede im Draft verbatim erhaltene Position einer Person als eigenes `<blockquote>Position…<cite>Name/Rolle</cite></blockquote>`. Beide/alle Seiten eines Collisions bleiben nebeneinander stehen, nicht zusammengefasst.
- **Warnungen** (Zeilen aus dem eingebetteten `rank_assumptions.py`-Output, die mit `WARNING:` oder `NOTE:` beginnen — insb. der Demand-Check): als
  ```html
  <div class="callout">
    <span class="callout-label">Warnung — Demand Check</span>
    <p>Text ohne das Präfix "WARNING:"/"NOTE:"</p>
  </div>
  ```
  Label anpassen falls die Warnung nicht den Demand-Check betrifft (z. B. "Warnung — Fiction Cap").
- Alles andere: Fließtext in `<p>`.

**Nichts weglassen.** Auch lange Abschnitte (Evidence Gaps, Ambiguities, Facilitator Notes) vollständig übernehmen — das ist ein Arbeitsdokument, keine Zusammenfassung.

### 5. Schreiben

Output-Pfad: im selben Run-Ordner, neben der Quelle: `<run>/7_final/PTW-Report.html`.

### 6. Bestätigen

```
Report geschrieben: <pfad>
[N] Abschnitte · Kunde: [Kunde] · Stand: [Datum]
```
