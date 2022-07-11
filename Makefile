project_name := bsw-test
compose_file := docker-compose.yml
compose := docker-compose -p $(project_name) -f $(compose_file)

create_network:
	docker network create bsw-test

b: build
build:
	$(compose) build $(args)

u: install
up: install
run: install
install:
	$(compose) up -d $(args)

bu: build_and_install
build_and_up: build_and_install
build_and_install:
	$(compose) up -d --build $(args)

rm: remove
remove:
	$(compose) rm -fs $(args)

stop:
	$(compose) stop $(args)

start:
	$(compose) start $(args)

restart:
	$(compose) restart $(args)

ps:
	$(compose) ps $(args)

psa:
	$(compose) ps -a

t: top
top:
	$(compose) top $(args)


sdl: show_docker_logs
show_docker_logs:
	$(compose) logs -f $(args)

gc: generate_configs
generate_configs:
	cp configs/db.env.example configs/db.env
	cp configs/pgadmin.env.example configs/pgadmin.env
	cp configs/bet-maker.env.example configs/bet-maker.env
	cp configs/line-provider.env.example configs/line-provider.env

style:
	black microservices
	isort microservices

migrate:
	$(compose) exec $(service) alembic upgrade head

makemigrations:
	$(compose) exec $(service) alembic revision --autogenerate -m "$(title)"

downmigrate:
	$(compose) exec $(service) alembic downgrade base

copy_migrate_line_provider:
	docker cp bsw-line-provider:/line-provider/migrations/versions microservices/line-provider/migrations

copy_migrate_bet_maker:
	docker cp bsw-bet-maker:/bet-maker/migrations/versions microservices/bet-maker/migrations
