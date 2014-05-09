#!/bin/bash
cd

if [ setup_done does not exist ]; then
    pip install -q --user -r tool/requirements.txt
    echo 'Done' > setup_done
fi
