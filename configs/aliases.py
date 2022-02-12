# by using list, we skip the call to parser = resulted in some speedup
fsi = "dotnet fsi"
dtest = "docker-compose -f docker-compose.yml -f docker/docker-compose.test.yml"
dprod = "docker-compose -f docker-compose.yml -f docker/docker-compose.prod.yml"
dstag = "docker-compose -f docker-compose.yml -f docker/docker-compose.stag.yml"
mem = "smem -ktP"
# code = "code-insiders"


# bat = "bat --terminal-width -5"
# less = 'bat --paging=always --pager "less -RF"'
ls = "exa"
diff = "colordiff"
tmux = "tmux -2"  # Force 256 colors
jq = "jq -C"  # Force colors
# rg = "rg --color always"  # Force color # ripgrep

# ssh = "kitty +kitten ssh"
