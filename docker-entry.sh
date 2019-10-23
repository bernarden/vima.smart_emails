#!/bin/bash

# Creating cron file from env variables.
env_cron_varible="CronSmartEmailSchedule"
auto_gen_cron_directory="/etc/cron.d/auto/"
env_cron_file_name="${auto_gen_cron_directory}env-smart-emails"
mapfile -t smart_email_schedules < <(printenv | grep -i $env_cron_varible)
if [[ ${#smart_email_schedules[@]} -ne 0 ]]; 
then
    echo "Found ${#smart_email_schedules[@]} email schedule(s) specified through environment variables."
    rm -rf $auto_gen_cron_directory
    for smart_email_schedule in "${smart_email_schedules[@]}"
    do
        regex="$env_cron_varible.*=(.*);\s*(.*)"
        if [[ $smart_email_schedule =~ $regex ]];
        then
            cron_expression="${BASH_REMATCH[1]}"
            drive="${BASH_REMATCH[2]}"

            if [[ ! -f $env_cron_file_name ]];
            then
                mkdir -p $auto_gen_cron_directory
                touch $env_cron_file_name
                echo "# This file is auto-generated. Don't add anything here manually!" >> $env_cron_file_name
            fi

            echo "$cron_expression sudo PYTHONPATH=/opt/vima.smart.emails/ python3 -m smart_emails $drive > /proc/1/fd/1 2>/proc/1/fd/2" >> $env_cron_file_name
            echo "" >> $env_cron_file_name
            echo "Env variable '$smart_email_schedule' added to cron config."
        else
            echo "Env variable '$smart_email_schedule' doesn't match regex and thefore won't be added to cron config."
        fi
    done
   
else
    echo "No email schedules were specified through environment variables."
fi

# Adding all files in /etc/cron.d/ to crontab.
cron_files=($(find /etc/cron.d/ -type f -not -path '*/\.*'))
if [[ ${#cron_files[@]} -ne 0 ]]; 
then
    for cron_file in $cron_files
    do
        echo "Adding file '$cron_file' to crontab."
        chmod 0644 $cron_file
        crontab $cron_file
    done

    echo "Configuration is completed."
    cron -f
else
    echo "Configuration failed. No cron files are configured."
fi
