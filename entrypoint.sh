#!/bin/sh

# Check if the main.py file exists in the host volume
if [ ! -f /usr/src/app/main.py ]; then
    echo "Initializing host volume with container files..."
    cp -r /usr/src/app-init/* /usr/src/app/
fi

# Execute the CMD
exec "$@"
