printf "Tag: "
read tag

./build.sh main.go
gh release create $tag --generate-notes bin/app/*
