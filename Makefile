
setup:
	python3 setup.py install --user
	python3 -m pip install --upgrade pip

	pip install selenium==4.0.0

	#sudo apt-get install firefox-geckodriver
	#sudo apt-get install chromium-browser
	#sudo apt install chromium-chromedriver


run_data_acquisition: 
	python3 src/hostelprices/datataking.py