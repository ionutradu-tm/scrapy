#!/bin/bash

if [[ -z $MAILFROM ]] || [[ -z $SMTP_HOST ]] || [[ -z SMTP_PORT ]] || [[ -z $SMTP_TO ]] || [[ -z $SMTP_SUBJECT ]];
   then
       export SEND_EMAIL=0
   else
       export SEND_EMAIL=1
fi

if [[ -n $HOSTNAME ]] && [[ -n $IP ]]; then                       # Loadbalancer IP + Hostname, set in host file
   echo "$IP $HOSTNAME" >> /etc/hosts
fi

if [[ -z $DEPTH ]]; then                                          # Recursivity level ("0" = unlimited)
   export DEPTH="2";
fi

if [[ -z $START_PAGES_ONLY ]]; then
   export START_PAGES_ONLY="no";
fi

if [[ -z $X_CACHE_UPDATER ]]; then                                # Defined in ordert to apply different actions
   export X_CACHE_UPDATER="1";
fi

if [[ -z $LOCALE ]]; then                                         # # Locales that will be scraped
   export LOCALE="";
fi

if [[ -z $AUTH_USER ]]; then
   export AUTH_USER="admin";
fi

if [[ -z $AUTH_PASSWORD ]]; then
   export AUTH_PASSWORD="password";
fi

if [[ -z $START_URLS ]]; then                                     # The URL from where the scraper will start
   echo "Please define START_URLS";
   exit 1;
fi

if [[ -z $CONCURRENT_REQUESTS_PER_IP ]]; then                     # Number of requests send at once
   export CONCURRENT_REQUESTS_PER_IP="1";
fi

if [[ -z $CLOSESPIDER_TIMEOUT ]]; then                            # Timeout of the job (it will be automatically stoped in 86400 seconds [24 hours])
   export CLOSESPIDER_TIMEOUT="0";
fi

if [[ -z $PEAK_AI_DAY ]]; then                                    # Day of the week when the warmup for PEAK_AI_COMPONENTS will run
   PEAK_AI_DAY="2";
fi

day=$(date +%u)                                                   # Current day

if [[ $day == "$PEAK_AI_DAY" && $RUN_PEAK_AI_COMPONENTS == "yes" ]]; then
   export RUN_PEAK_AI_COMPONENTS="yes";
else
   export RUN_PEAK_AI_COMPONENTS="no";
fi

export RUN_SHOP="${RUN_SHOP:-no}"
export DEBUG_LEVEL="${DEBUG_LEVEL:-DEBUG}"
python3 /scraper.py
