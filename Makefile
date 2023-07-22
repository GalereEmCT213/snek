cache_files := */*/__pycache__ ./*/.ipynb_checkpoints ./*/.DS_Store venv/ .idea/ .pytest_check/ .vscode/
zip_name = grupo1_exame
zip_ext = .zip

all: zip

clean:
	rm -rf $(cache_files)

zip: clean
	zip -r $(zip_name)$(zip_ext) * -x $(cache_files)