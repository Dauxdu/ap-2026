.PHONY: init lab_01 lab_02

init:
	pip install --upgrade pip && pip install -r requirements.txt

lab_01:
	python3 lab/lab_01/main.py lab/lab_01/data/input.txt -o lab/lab_01/data/output.txt

lab_02:
	python3 lab/lab_02/main.py 3 lab/lab_02/data lab/lab_02/data/annotation.csv
