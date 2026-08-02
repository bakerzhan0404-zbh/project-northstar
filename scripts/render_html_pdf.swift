import AppKit
import Foundation

guard CommandLine.arguments.count == 3 else {
    fputs("Usage: render_html_pdf.swift <html-fragment> <output-pdf>\n", stderr)
    exit(2)
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
let fragment = try String(contentsOf: inputURL, encoding: .utf8)

let html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: A4; margin: 18mm; }
body { font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; color: #172033; font-size: 10.5pt; line-height: 1.42; }
h1 { color: #17365d; font-size: 23pt; margin: 0 0 15pt; padding-bottom: 8pt; border-bottom: 2px solid #c8a45d; }
h2 { color: #17365d; font-size: 15pt; margin: 18pt 0 7pt; }
p { margin: 5pt 0 8pt; }
table { width: 100%; border-collapse: collapse; margin: 9pt 0 12pt; font-size: 9pt; }
th { background: #17365d; color: white; font-weight: 600; text-align: left; }
th, td { border: 1px solid #cbd3df; padding: 5pt 6pt; vertical-align: top; }
tr:nth-child(even) td { background: #f4f7fa; }
pre { background: #f1f3f5; border-left: 3px solid #c8a45d; padding: 8pt; font-family: Menlo, monospace; font-size: 8.5pt; white-space: pre-wrap; }
code { font-family: Menlo, monospace; font-size: 9pt; }
ul, ol { margin: 5pt 0 9pt 18pt; }
li { margin: 2pt 0; }
</style>
</head>
<body>\(fragment)</body>
</html>
"""

let data = Data(html.utf8)
let attributed = try NSAttributedString(
    data: data,
    options: [
        .documentType: NSAttributedString.DocumentType.html,
        .characterEncoding: String.Encoding.utf8.rawValue,
    ],
    documentAttributes: nil
)

let printInfo = NSPrintInfo()
printInfo.paperSize = NSSize(width: 595.28, height: 841.89)
printInfo.topMargin = 51
printInfo.bottomMargin = 51
printInfo.leftMargin = 51
printInfo.rightMargin = 51
printInfo.horizontalPagination = .fit
printInfo.verticalPagination = .automatic
printInfo.jobDisposition = .save
printInfo.dictionary()[NSPrintInfo.AttributeKey.jobSavingURL] = outputURL

let pageWidth = printInfo.imageablePageBounds.width
let textView = NSTextView(frame: NSRect(x: 0, y: 0, width: pageWidth, height: 10_000))
textView.isEditable = false
textView.isSelectable = false
textView.isHorizontallyResizable = false
textView.isVerticallyResizable = true
textView.textContainer?.containerSize = NSSize(width: pageWidth, height: .greatestFiniteMagnitude)
textView.textContainer?.widthTracksTextView = true
textView.textStorage?.setAttributedString(attributed)
textView.layoutManager?.ensureLayout(for: textView.textContainer!)

if let used = textView.layoutManager?.usedRect(for: textView.textContainer!) {
    textView.frame.size.height = max(used.height + 40, printInfo.imageablePageBounds.height)
}

let operation = NSPrintOperation(view: textView, printInfo: printInfo)
operation.showsPrintPanel = false
operation.showsProgressPanel = false
guard operation.run() else {
    fputs("PDF generation failed\n", stderr)
    exit(1)
}

print("Wrote \(outputURL.path)")
