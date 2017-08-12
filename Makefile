########################################################################
#
# (C) 2016, Blaz Divjak, ARNES <blaz@arnes.si> <blaz@divjak.si>
#
# This file is part of Automator
#
# Automator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Automator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Automator.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

SHELL := /bin/bash

.DEFAULT_GOAL := help
.PHONY: help
help: ## Prints this text
	@printf "\nUsage: <VARIABLES> make <TARGET>\n"
	@printf "\nTargets:\n\n"
	@grep -E '^[a-zA-Z_/%\-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@printf "\n"

build: ## Builds automator docker image	
	@echo "#### Building automator image"
	docker build . -t automator

run: clean ## Starts automator server and dependencies
	docker run -d -p 5672:5672 --name rabbitmq rabbitmq
	docker run -d -p 8000:8000 -v $(CURDIR):/opt/automator --name automator automator
	docker exec -it automator bash -c "cd lib/openconfig && ./openconfig.sh"
	docker run -d -v $(CURDIR):/opt/automator --name celery automator celery -A automator worker -l info
	docker run -d -p 5555:5555 -v $(CURDIR):/opt/automator --name flower automator celery -A automator flower --port=5555
	docker exec automator python manage.py migrate
	docker exec -it automator python manage.py createsuperuser --username admin --email admin@admin.si
	docker exec automator python manage.py createcachetable
	docker exec automator python manage.py collectstatic --noinput

clean: ## Stop and clean	
	-docker rm -f rabbitmq
	-docker rm -f automator
	-docker rm -f celery
	-docker rm -f flower

reset-db: ## Resets database
	docker exec automator python manage.py reset_db --noinput

test: ## Runs tests
	docker exec automator python manage.py test --noinput
