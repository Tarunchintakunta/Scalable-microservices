#!/bin/bash

# Start all services using tmux
# Requires tmux to be installed: brew install tmux

if ! command -v tmux &> /dev/null; then
    echo "tmux is not installed. Please install it first:"
    echo "  macOS: brew install tmux"
    echo "  Linux: sudo apt-get install tmux"
    exit 1
fi

SESSION="ecommerce"

# Create new tmux session
tmux new-session -d -s $SESSION

# Window 0: Service A
tmux rename-window -t $SESSION:0 'Service-A'
tmux send-keys -t $SESSION:0 'cd services/service-a-identity-commerce && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001' C-m

# Window 1: Service B
tmux new-window -t $SESSION:1 -n 'Service-B'
tmux send-keys -t $SESSION:1 'cd services/service-b-catalog-fulfillment && source .venv/bin/activate && uvicorn app.main:app --reload --port 8002' C-m

# Window 2: Service C
tmux new-window -t $SESSION:2 -n 'Service-C'
tmux send-keys -t $SESSION:2 'cd services/service-c-notifications-serverless && source .venv/bin/activate && uvicorn app.main:app --reload --port 8010' C-m

# Window 3: Frontend
tmux new-window -t $SESSION:3 -n 'Frontend'
tmux send-keys -t $SESSION:3 'cd frontend && npm run dev' C-m

# Attach to session
tmux attach-session -t $SESSION
