#!/bin/bash
cd

if [ ! -f "setup_done" ]; then
    pip install -q --user -r tool/requirements.txt
    echo 'Done' >> setup_done
fi
