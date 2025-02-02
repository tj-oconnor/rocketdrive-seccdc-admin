DOCKER_USER=tjoconnor
DEMO_TAG=rocketdrive-demo
LIVE_TAG=rocketdrive-live

APP_FILES=app/files/
DEMO_FILES=demo_files/
LIVE_FILES=live_files/

.PHONY: all demo live clean
all: demo live

.PHONY: demo
demo:
	@echo "Building demo environment..."
	rm -rf app/db/users.db
	python3 init_demo_db.py
	rm -rf $(APP_FILES)*/
	cp -r $(DEMO_FILES)/* $(APP_FILES)
	docker build -t $(DEMO_TAG) .
	docker tag $(DEMO_TAG) $(DOCKER_USER)/$(DEMO_TAG)
	docker push $(DOCKER_USER)/$(DEMO_TAG)
	@echo "Demo image built and committed to $(DOCKER_USER)/$(DEMO_TAG)"

.PHONY: live
live:
	@echo "Building live environment..."
	rm -rf app/db/users.db
	python3 init_live_db.py
	rm -rf $(APP_FILES)*/
	cp -r $(LIVE_FILES)/* $(APP_FILES)
	docker build -t $(LIVE_TAG) .
	docker tag $(LIVE_TAG) $(DOCKER_USER)/$(LIVE_TAG)
	docker push $(DOCKER_USER)/$(LIVE_TAG)
	docker save -o live-image $(LIVE_TAG)
	@echo "Live image built, committed, and saved as live-image"

.PHONY: clean
clean:
	@echo "Cleaning up temporary files..."
	@echo rm -rf $(APP_FILES)*/
