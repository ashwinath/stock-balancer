.PHONY = setup
setup:
	python3 -m pip install -r requirements.txt

.PHONY = proto
proto:
	protoc --python_out=./generated proto/*.proto
