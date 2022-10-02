init:
	docker-compose run web scripts/init.sh

migrations:
	docker-compose run web scripts/migrations.sh

migrate:
	docker-compose run web scripts/migrate.sh

test:
	docker-compose run web scripts/test.sh

auction:
	docker-compose run web scripts/auction.sh

superuser:
	docker-compose run web scripts/superuser.sh