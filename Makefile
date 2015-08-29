install-libs:
	# pip install everything in requirements.txt to lib
	pip install -t lib -r lib_requirements.txt


deploy-app:
	#deploys to dev
	deployer/shell.py --build_path=./ --app=nfl-database --app_version=init \
	-v -i -d -q -c --modules app admin crime
