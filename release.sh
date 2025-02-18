printf "Tag: "
tag=$(read)

./build.sh main.go
gh release create $tag --notes "precompiled bins" bin/app/*
