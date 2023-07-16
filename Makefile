# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down clone wheels build

elastic:
	docker-compose up -d elastic

# clone:
# 	./clone.sh

# wheels:
# 	./wheels.sh

# build:
# 	sh ./build.sh

# up:
# 	docker-compose up -d

# rekcart:
# 	docker-compose up -d rekcart

# docker-compose-down:
# 	docker-compose down --remove-orphans

# down:
# 	bash ./down.sh

# db:
# 	bash ./setup-postgres-db.sh