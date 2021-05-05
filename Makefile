.PHONY: build
build:
	sam-beta-cdk build --parallel -u --cached --skip-pull-image	

.PHONY: api
api:
	sam-beta-cdk build --parallel -u --skip-pull-image	
	sam-beta-cdk local start-api --skip-pull-image --warm-containers EAGER

.PHONY: invoke
invoke:
	sam-beta-cdk build --parallel -u --skip-pull-image	
	sam-beta-cdk local invoke CDKML/t5large
