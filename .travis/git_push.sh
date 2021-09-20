#!/bin/bash

set -e
## Add custom git config
git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis CI"


## Ensure git URL contains github access token
git_url_with_token=$(git remote get-url origin | sed -e "s/github.com/${GITHUB_ACCESS_TOKEN}:github.com/g")
git remote set-url origin $git_url_with_token

## Push modifications
git push origin HEAD:$TRAVIS_BRANCH