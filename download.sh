#!/bin/bash
echo "------------------------------------"
echo "----- STARTING DOWNLOAD SCRIPT -----"
FILEID=1SLH_QntBxyrtjvYarWA5Q1H6DexBN8ER
FILENAME=data.zip
echo "------------------------------------"
echo "---- 1. Getting data from Drive ----"
echo "IMPORTANT: Be sure to have at least a 30 GB amount of free space in your disk !!!"
echo "------------------------------------"
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=${FILEID}" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${FILEID}" -O ${FILENAME} && rm -rf /tmp/cookies.txtz
echo "------------------------------------"
echo "---- 2. Starting unziping data! ----"
echo "------------------------------------"
unzip data.zip
echo "------------------------------------"
echo "---- 3.    Removing data.zip    ----"
echo "------------------------------------"
rm data.zip
echo "------------------------------------"
echo "Congrats, you can start the scripts!"
echo "------------------------------------"
