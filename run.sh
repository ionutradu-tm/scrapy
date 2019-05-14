#!/bin/bash

if [[ -z $MAILFROM ]] || [[ -z $SMTP_HOST ]] || [[ -z SMTP_PORT ]] || [[ -z $SMTP_TO ]] || [[ -z $SMTP_SUBJECT ]];
   then
       export SEND_EMAIL=0
   else
       export SEND_EMAIL=1
fi

if [[ -n $HOSTNAME ]] && [[ -n $IP ]]; then
   echo "$IP $HOSTNAME" >> /etc/hosts
fi

if [[ -z $DEPTH ]]; then
   export DEPTH="2";
fi

if [[ -z $START_PAGES_ONLY ]]; then
   export START_PAGES_ONLY="no";
fi

if [[ -z $DEPTH ]]; then
   export DEPTH="2";
fi

if [[ -z $X_CACHE_UPDATER ]]; then
   export X_CACHE_UPDATER="1";
fi

if [[ -z $LOCALE ]]; then
   export LOCALE="";
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

RUN_SHOP="${RUN_SHOP:-no}"
python3 /scraper.py
