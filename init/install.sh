#! /bin/bash
echo 'installing fixture_server now'
cp fixture_server.service /etc/systemd/system
systemctl enable fixture_server.service
systemctl start fixture_server.service
systemctl | grep AKA