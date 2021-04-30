# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

build:
	docker build --network=host . -t docker.pkg.github.com/narcismpap/labx/labx:latest

run:
	docker run --rm docker.pkg.github.com/narcismpap/labx/labx:latest

test: 
	docker run --rm -v $(ROOT_DIR)/labx:/labx/code --entrypoint pytest docker.pkg.github.com/narcismpap/labx/labx:latest -v

black:
	docker run --network none --rm -v $(ROOT_DIR)/labx:/data cytopia/black -l 120 .

