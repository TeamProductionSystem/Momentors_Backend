#!/bin/bash

branch_name=$(git rev-parse --abbrev-ref HEAD)


regex="^(feature|bugfix|hotfix|chore|test)/(issue-[0-9]+|no-ref)/[a-z0-9\-]+$"

if [[ ! $branch_name =~ $regex ]]; then
    echo "Error: Branch name does not match the required format!"
    echo "Expected Format: <category>/<reference>/<description-in-lower-case>"
    echo "Example: chore/issue-1/test"
    exit 1
fi