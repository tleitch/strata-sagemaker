.PHONY: reproduce verify tables figures significance disparity
reproduce: verify tables figures significance disparity
tables:
	python evaluation/reproduce_tables.py
figures:
	python evaluation/plot_figures.py
significance:
	python evaluation/compute_significance.py
disparity:
	python evaluation/compute_disparity.py
verify:
	python evaluation/verify_checksums.py CHECKSUMS.md
