.DEFAULT_GOAL := default
proj = "plugin.video.tide"
version = "0.3.1"

default:
	git archive --prefix=$(proj)/ leia -o $(proj)-$(version).zip

install:
	git ls-files --others --exclude-standard --cached | zip --names-stdin latest.zip
	unzip -o latest.zip -d ~/.var/app/tv.kodi.Kodi/data/addons/${proj}

clean:
	rm *.zip *.pyc
