HUGO = hugo
COMMIT_MESSAGE = "rebuilding site $(shell date +%Y-%m-%d)"

run:
	$(HUGO) server -D --bind=0.0.0.0

dev:
	$(HUGO) server -D --bind=0.0.0.0 --disableFastRender

clone:
	rm -rf public
	git clone https://github.com/gyuha/gyuha.github.io.git
	mv gyuha.github.io public

new:
	$(HUGO) new post/$(shell date +%Y-%m-%d)-$(title).md

deploy:
	echo "\033[0;32mDeploying updates to GitHub...\033[0m"

	# Build the project.
	$(HUGO) -D

	cd ./public && git add . && git commit -m $(COMMIT_MESSAGE) && git push
	git commit -am "update" && git push
