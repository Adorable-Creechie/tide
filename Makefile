.DEFAULT_GOAL := default
proj = "plugin.video.tide"
version = "0.1.5"

default:
	git archive --prefix=$(proj)/ master -o $(proj)-$(version).zip

install:
	git ls-files --others --exclude-standard --cached  | zip --names-stdin latest.zip
	unzip -o latest.zip -d ~/.kodi/addons/${proj}

clean:
	rm *.zip *.pyc
