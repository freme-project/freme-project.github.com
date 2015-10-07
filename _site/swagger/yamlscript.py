#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# This script, when run, parses the file "swagger.yaml" and strips it down to only
# include those paths and methods specified in the included variable.
#
# As of now, it is called with every "jekyll build" - see jekyll-freme/_plugins/jekyll-pages-directory.rb
# line: "exec(python swagger/yamlscript.py)"
#
# To be able to import yaml, on linux, run "sudo pip install PyYAML"
#
# Author: Jonathan Sauder (jonathan_paul.sauder@dfki.de)
#


def main():
	import yaml,os,sys
	try:
		with open(os.path.dirname(__file__)+"/swagger.yaml","r") as f:
			full=yaml.safe_load(f.read())
	except IOError:
		raise Exception("\n\tException Handled in /swagger/yamlscript.py:"+ os.path.dirname(__file__)+"/swagger.yaml could not be found. The generation of a simple API-Doc was skipped")
		sys.exit(1)
	except yaml.scanner.ScannerError:
		raise Exception("\n\tException Handled in /swagger/yamlscript.py: The YAML File at "+ os.path.dirname(__file__)+"/swagger.yaml is invalid! The generation of a simple API-Doc was skipped")	
		sys.exit(1)
		
	included={
	"/e-entity/freme-ner/documents": ["post"],
	"/e-entity/dbpedia-spotlight/documents": ["post"],
	"/e-publishing/html": ["post"],
	"/e-link/documents/": ["post"],
	"/e-translation/tilde": ["post"],	
	"/e-terminology/tilde": ["post"]
	}
	
	for path in full["paths"].keys():
		if path not in included:
			del full["paths"][path]
		else:
			for method in included[path]:
				if method not in full["paths"][path].keys():
					del full["paths"][path][method]
				else:
					full["paths"][path][method]['tags']=["Enrichment Endpoints"]
	
	full['info']['description']="This section only covers the most important endpoints of FREME: the enrichment endpoints. <br> A full Documentation is provided <a href=\"full.html\"> here</a>."
	
	
	with open(os.path.dirname(__file__)+"/simple.yaml",'w') as f:
		f.write(yaml.dump(full))
	return 0

		
if __name__ == '__main__':
	main()

