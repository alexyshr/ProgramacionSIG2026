@echo off
echo Limpiando proyecto Quarto...

if exist _site rmdir /s /q _site
if exist .quarto rmdir /s /q .quarto
if exist _cache rmdir /s /q _cache
if exist _freeze rmdir /s /q _freeze

del /q *.aux *.log *.toc *.out *.bbl *.blg *.lof *.lot 2>nul
del /q *.synctex.gz *.fdb_latexmk *.fls 2>nul

echo Proyecto limpio.
pause