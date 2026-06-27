# Fast local Jekyll preview.
#
# Layers _config_dev.yml on top of _config.yml, which excludes
# assets/images/exhibit-images (~4,000 files / 273 MB) from the build so
# it doesn't get re-copied into _site every time. Those exhibit images
# will 404 in the preview — that's expected.
#
# Working on exhibit images? Run a normal full build instead:
#   bundle exec jekyll serve
#
# Any extra args you pass are forwarded to jekyll, e.g.:
#   .\serve-fast.ps1 --incremental
#   .\serve-fast.ps1 --port 4001

bundle exec jekyll serve --config _config.yml,_config_dev.yml @args