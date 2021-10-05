all: dissertation frontpage

dissertation:
	pdflatex dissertation
	bibtex dissertation
	pdflatex dissertation
	pdflatex dissertation

frontpage:
	pdflatex frontpage

dependencies: dissertation
	pdflatex -recorder dissertation

.PHONY: clean
clean:
	rm -f dissertation.pdf dissertation.ps dissertation.fls *.aux *.log *.bbl *.blg *.lof *.lot *.toc *.out *.fdb_latexmk
	rm -f contents/*.fls contents/*.aux contents/*.log contents/*.bbl contents/*.blg contents/*.lof contents/*.lot contents/*.toc contents/*.out contents/*.fdb_latexmk
	rm -f frontpage.pdf
