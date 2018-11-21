WIKIDUMP :=  http://dumps.wikimedia.org/itwiki/latest/itwiki-latest-pages-articles.xml.bz2


.ONESHELL:
wikiextractor:
	@if [ ! -d "wikiextractor" ]; then \
		git submodule add --force https://github.com/attardi/wikiextractor.git; \
		cd wikiextractor; \
		sudo python3 setup.py install; \
		cd .. ; \
	fi

wikidata: wikiextractor
	sudo chmod u+x scripts/data/download_and_extract_wiki.sh; \
	./scripts/data/download_and_extract_wiki.sh \
		$(WIKIDUMP) wikiextractor/WikiExtractor.py;
