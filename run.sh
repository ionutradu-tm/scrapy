#!/bin/bash


if [[ -n $HOSTNAME ]] && [[ -n $IP ]]; then
   echo "$IP $HOSTNAME" >> /etc/hosts
fi

if [[ -z $DEPTH ]]; then
   export DEPTH="2";
fi

if [[ -z $DEPTH ]]; then
   export DEPTH="2";
fi

if [[ -z $X-CACHE-UPDATER ]]; then
   export X-CACHE-UPDATER="1";
fi

python3 /scraper.py
