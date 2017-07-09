
.PHONY: setup

ssh_conf_path = ~/.ssh/
files_path    = ./files/

setup: $(files_path)develop/id_rsa.github

$(files_path)develop/id_rsa.github:
	cp $(ssh_conf_path)id_rsa $@
