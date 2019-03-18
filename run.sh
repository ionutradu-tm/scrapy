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

if [[ -z $X_CACHE_UPDATER ]]; then
   export X_CACHE_UPDATER="1";
fi

if [[ -z $AUTH_USER ]]; then
   export AUTH_USER="admin";
fi

if [[ -z $AUTH_PASSWORD ]]; then
   export AUTH_PASSWORD="password";
fi

if [[ -z $START_URLS ]]; then
   echo "Please define START_URLS";
   exit 1;
fi

if [[ -z $CONCURRENT_REQUESTS_PER_IP ]]; then
   export CONCURRENT_REQUESTS_PER_IP 0;
fi

if [[ -z $CLOSESPIDER_TIMEOUT   ]]; then
   export  CLOSESPIDER_TIMEOUT 0;
fi

python3 /scraper.py
