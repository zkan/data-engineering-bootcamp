VOLUME_NAME = $(shell docker volume ls | grep getting-started-with-analytics-engineering | awk '{print $$2}')

up:
	docker-compose up -d

down:
	docker-compose down

remove_volume:
	docker volume rm $(VOLUME_NAME)

clean: down remove_volume

restart: down up

reset: down remove_volume up

restart: down up
