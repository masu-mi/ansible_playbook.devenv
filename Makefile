
.PHONY: setup

ssh_conf_path = ~/.ssh/
files_path    = ./files/

setup: $(files_path)develop/id_rsa.github
	ansible-galaxy -r ./requirements.yml install

$(files_path)develop/id_rsa.github:
	cp $(ssh_conf_path)id_rsa $@
