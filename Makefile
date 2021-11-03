post-convert: cleanup-bids install-events validate

basedir = "/home/poldrack//data/fmri-handbook-2e-data/bids"

validate:
	bids-validator $(basedir)

# clean up various issues with bids dataset
cleanup-bids:
	# get rid of events files for rest datasets
	-find $(basedir) -name "*rest*events.tsv" -exec rm {} \;
	-find $(basedir) -name "*retinotopy*events.tsv" -exec rm {} \;
	# make writable
	find $(basedir) -name "*.json" -exec chmod +w {} \;
	# fix json files
	python fix_json_files.py
	python mk_events_json.py
	# change back to ro
	find $(basedir) -name "*.json" -exec chmod -w {} \;

install-events:
	# install event.tsv files for tasks

	# make writable
	find $(basedir) -name "*.tsv" -exec chmod +w {} \;
	
	# install event files
	python install_events.py
	# change back to ro
	find $(basedir) -name "*.trsv" -exec chmod -w {} \;

