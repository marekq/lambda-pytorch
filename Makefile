.PHONY: build
build:
	sam build --parallel -u --cached

.PHONY: init
init:
	sam build --parallel -u --cached
	sam deploy -g

.PHONY: deploy
deploy:
	sam build --parallel -u --cached
	sam deploy

.PHONY: local
local:
	sam build --parallel -u --cached
	sam local invoke 
