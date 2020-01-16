STACK_NAME ?= devbox-spot
SSH_KEY ?= $(HOME)/.ssh/id_rsa
USERNAME ?= ubuntu

all: build deploy

setup:
	$(info [*] Installing python requirements)
	@pip install -r requirements.txt

build:
	$(info [*] Building Lambda functions)
	@sam build

deploy:
	$(info [*] Deploying stack)
	@sam deploy

start:
	$(info [*] Starting devbox)
	@scripts/devbox start $(STACK_NAME)

status:
	$(info [*] Checking devbox status)
	@scripts/devbox status $(STACK_NAME)

connect:
	$(info [*] Connecting to the instance)
	@ssh -i $(SSH_KEY) $(USERNAME)@$(shell scripts/devbox status $(STACK_NAME) | jq '.dns')