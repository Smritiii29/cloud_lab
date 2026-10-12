nano script.sh

for i in {1..6}; do
    echo "Hello Selcia" >> /home/ubuntu/output.log
    sleep 10
done

chmod +x script.sh

crontab -e

* * * * * /home/ubuntu/script.sh

tail -f /home/ubuntu/output.log

cat /home/ubuntu/output.log (Verification)