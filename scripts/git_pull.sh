#!/bin/sh
exec 2>&1
. $(dirname $(readlink -f $0))/config.sh

cd $public_html_session_directory/private
if git pull origin master
then
        :
else
        git stash
        if git pull origin master
        then
                :
        else
            git fetch --all
            if git reset --hard origin/master
            then
                $scripts_directory/build
            else
                git pull origin master 2>&1 |mail -s 'pull failed' andrewt
                exit 1
            fi
        fi
fi
(       git diff --summary 'HEAD^!'
        git log -1 --stat
        git diff --diff-filter=M 'HEAD^!'|sed 128q
)|mail -s "pull succeeded: `git log -1 --name-only|sed 1,6d`" andrewt
