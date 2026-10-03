.PHONY: init lab_01 lab_02 lab_03

init:
	pip install --upgrade pip && pip install -r requirements.txt

lab_01:
	python3 lab/lab_01/main.py lab/lab_01/data/input.txt -o lab/lab_01/data/output.txt

lab_02:
	python3 lab/lab_02/main.py 3 lab/lab_02/data lab/lab_02/data/annotation.csv

lab_03:
	python3 lab/lab_03/main.py lab/lab_02/data/Travel/0001.jpg lab/lab_02/data/Classics/0001.jpg lab/lab_03/data/result.jpg --width 200 --height 400 --angle 45
