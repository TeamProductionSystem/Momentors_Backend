#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat $commit_msg_file)

regex_without_scope="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert): .+$"
regex_with_scope="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)\([a-z]+\): .+$"

if [[ ! $commit_msg =~ $regex_with_scope ]] && [[ ! $commit_msg =~ $regex_without_scope ]]; then
    echo "Error: Commit message does not match the required format!"
    echo "Expected Format: <category(scope): description>"
    echo "Example: chore(test): setup test"
    exit 1
fi
