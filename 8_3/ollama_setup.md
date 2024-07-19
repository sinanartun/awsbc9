1. install ollama 

```
curl -fsSL https://ollama.com/install.sh | sh
```

2. Edit the Ollama Service
```
sudo systemctl edit ollama.service
```
3. paste service settings into new service config file
```
[Service]
Environment="OLLAMA_HOST=0.0.0.0:8080"
Environment="OLLAMA_ORIGINS=*"
```
4. Restart Ollama service
```
sudo systemctl daemon-reload
sudo systemctl restart ollama.service
sudo systemctl status ollama.service
```
5. Check if service Environment is set
```
systemctl show ollama.service | grep Environment
```
6. Edit ubuntu user settings
```
nano ~/.bashrc
```
7. insert this line at the bottom of the .bashrc file
```
export OLLAMA_HOST=0.0.0.0:8080
```
8. Swich user from ubuntu to root after that swich user again from root to ubuntu
```
sudo su
su ubuntu
```
9. Check if environment is set
```
echo $OLLAMA_HOST
```
10. download and run ollama model. this command will run model locally.
```
ollama run llama3:latest
```
11. serve ollama.service


```
ollama serve
```

12. Check if ollama.service is running
```
curl -X POST http://localhost:8080/api/generate -d '{
  "model": "llama3",
  "prompt":"what is 3 + 5 ?",
  "stream": false
 }'
```