sudo tee /etc/systemd/system/ekr.service <<EOF
[Unit]
Description=Expert Knowledge Repository
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/expert-knowledge-repository
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ekr
sudo systemctl start ekr
