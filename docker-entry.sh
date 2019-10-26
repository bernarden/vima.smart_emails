#!/bin/bash

echo "#!/bin/bash
. <(xargs -0 bash -c 'printf \"export %q\n\" \"\$@\"' -- < /proc/1/environ)
PYTHONPATH=/opt/vima.smart.emails/ python3 -m smart_emails \$1" > /tmp/execute_smart_emails.sh

# Creating cron file from env variables.
env_cron_varible="CronSmartEmailSchedule"
cron_directory="/etc/cron.d/"
env_cron_file_name="${cron_directory}auto-env-smart-emails"
mapfile -t smart_email_schedules < <(printenv | grep -i $env_cron_varible)
if [[ ${#smart_email_schedules[@]} -ne 0 ]]; 
then
    echo "Found ${#smart_email_schedules[@]} email schedule(s) specified through environment variables."
    rm -f env_cron_file_name
    for smart_email_schedule in "${smart_email_schedules[@]}"
    do
        regex="$env_cron_varible.*=(.*);\s*(.*)"
        if [[ $smart_email_schedule =~ $regex ]];
        then
            cron_expression="${BASH_REMATCH[1]}"
            drive="${BASH_REMATCH[2]}"

            if [[ ! -f $env_cron_file_name ]];
            then
                touch $env_cron_file_name
                echo "# This file is auto-generated. Don't add anything here manually!" >> $env_cron_file_name
                echo "SHELL=/bin/bash" >> $env_cron_file_name
            fi

            echo "$cron_expression root . /tmp/execute_smart_emails.sh $drive > /proc/1/fd/1 2>/proc/1/fd/2" >> $env_cron_file_name
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
cron_files=($(find $cron_directory -type f -not -path '*/\.*'))
if [[ ${#cron_files[@]} -ne 0 ]]; 
then
    for cron_file in $cron_files
    do
        echo "Updating permissions for cron's file: '$cron_file'."
        chmod 0644 "$cron_file"
    done

    echo "Configuration is complete."
    echo "------------------------------"
    cron -f
else
    echo "Configuration failed. No cron files are configured."
fi
