# LLMs on the Edge
Large-language models (LLMs) are on the pareto frontier of machine learning. Their size, however, makes them inaccessible to those with modest devices and limited compute resources. This project aims to bridge this gap by applying several model optimization techniques to reduce the computational complexity of LLMs, making them small enough, yet still powerful, to run on EDGE devices. We demonstrate this by hosting a Llama2 7-billion parameter model on an NVIDIA Jetson Xavier that allows chat-like interfacing through a portable UI. This project is part of UCF's Senior Design class sequence (i.e., COP 4934 & COP 4935).

## Meet the Team
* Christian Cooper - Project Manager
* Daniel Solis - Model R&D
* Michael Regis - Web
* Timothy Oei - Web
* Yeshwanth Mandava - Model R&D
* Zackary Kiener - Hardware & Model Optimization

## Sample Test
Start and attach to the provided docker container using your preferred method (e.g., VSCode's dev containers extension). Then, start the server using:
```
python3 src/server.py
```

Send a sample chat request to the model using:
```
curl -X POST -H "Content-Type: application/json" -d '{"system_msg": "You are my personal assistant! Please answer everything I ask respectfully", "prompt": "Why is the sky blue?"}' http://localhost:5000/api/chat
```