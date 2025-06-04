install:
	poetry install

setup:
	mkdir -p catalog

run:
	poetry run python main.py

run_gcs:
	poetry run python main_gcs.py

clean:
	rm -rf catalog/*
	poetry run python delete_gcs_folders.py
