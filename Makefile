.PHONY: reproduce verify figures tables
reproduce: verify tables figures
tables:
	python evaluation/reproduce_tables.py
figures:
	python evaluation/plot_figures.py
verify:
	python evaluation/verify_checksums.py CHECKSUMS.md
