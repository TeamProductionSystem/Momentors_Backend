#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat $commit_msg_file)

regex="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)\([a-z]+\): .+$"

if [[ ! $commit_msg =~ $regex ]]; then
    echo "Error: Commit message does not match the required format!"
    echo "Expected Format: <category(scope): description>"
    echo "Example: chore(test): setup test"
    exit 1
fi