#!/usr/bin/env bash


# OCR:
for f in ./*.pdf; do ocrmypdf "$f" "$(basename "$f" ".pdf")_ocr.pdf"; done
mkdir ocr
mv *_ocr.pdf ./ocr/

# PDF to text:
for f in ./*.pdf; do
NAME_OCR="./ocr/$(basename "$f" ".pdf")_ocr.pdf"
if test -f $NAME_OCR; then
    echo "using OCR'd pdf"
    pdftotext $NAME_OCR "$(basename "$f" ".pdf").txt"
else
    echo "no ocr"
    pdftotext "$f" "$(basename "$f" ".pdf").txt"
fi
done
mv *.txt ../amicus-briefs-text/

#htm files
textutil -convert txt *.htm
mv *.txt ../amicus-briefs-text/

# zip
# Note: some cd, mkdir, etc missing
zip downloads-amicus.zip -r  downloads-amicus
