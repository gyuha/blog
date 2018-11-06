HUGO = hugo
COMMIT_MESSAGE = "rebuilding site $(shell date +%Y-%m-%d)"


run:
	$(HUGO) server -D

new:
	$(HUGO) new post/$(shell date +%Y-%m-%d)-$(title).md

deploy:
	echo "\033[0;32mDeploying updates to GitHub...\033[0m"

	# Build the project.
	$(HUGO)

	cd public
	# Add changes to git.
	git add .
	git commit -m $(COMMIT_MESSAGE)

	# Push source and build repos.
	git push

	# Come Back up to the Project Root
	cd ..

