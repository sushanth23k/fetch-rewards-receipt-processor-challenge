workers = 4
bind = "0.0.0.0:8000"
chdir = "/app/src"
module = "fetch_rewards.wsgi:application"
timeout = 120