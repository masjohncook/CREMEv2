#!/bin/bash

SESSION="CREME"

tmux start-server

if [ "$(tmux ls | grep ${SESSION})" ]; then
  tmux kill-session -t ${SESSION}
fi

tmux new-session -d -s ${SESSION} -n CREME
tmux set remain-on-exit on
tmux split-window -h
tmux split-window -v -t 0


#terminal 0
tmux send-key -t 0 "cd ~/redis-stable/src" Enter
tmux send-key -t 0 "./redis-server" Enter

#terminal 1
tmux send-key -t 1 "cd ~/CREMEv2" Enter
tmux send-key -t 1 "source venv_CREMEv2/bin/activate" Enter
tmux send-key -t 1 "celery -A CREME.celery worker --loglevel=info > celery.log" Enter

#terminal 2
tmux send-key -t 2 "cd ~/CREMEv2" Enter
tmux send-key -t 2 "source venv_CREMEv2/bin/activate" Enter
tmux send-key -t 2 "python manage.py runserver 0.0.0.0:8000" Enter


tmux -2 attach-session -t ${SESSION}

