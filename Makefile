out/resolved.json: bin/resolved.py in/known.json tmp/*.pdb
	$^ > $@

doc: README.markdown
	markdown $^ > README.html
