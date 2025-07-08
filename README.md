🧭 Consistent Hashing Load Balancer with Docker and Flask

This project implements a simulated **Load Balancer** using **Consistent Hashing** with Docker containers acting as server replicas. It is designed to demonstrate key load balancing concepts including:
- Load distribution
- Fault tolerance
- Scalability
- Virtual servers
- Hash-based request routing

The project is structured around a custom consistent hash ring implementation, Docker-based server instances, and Flask-based routing logic.

---

📁 Project Structure



load\_balancer\_project/
│
├── analysis/               # Scripts and result graphs for A1–A3 analysis
│   ├── analyze\_a1.py
│   ├── analyze\_a2.py
│   ├── analyze\_a3.py
│   ├── a1\_results.png
│   ├── a2\_scalability.png
│   └── a3\_fault\_tolerance.png
│
├── server/                 # Dockerized simple Flask server replica
│   ├── server.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── src/                    # Load balancer and consistent hash logic
│   ├── load\_balancer.py
│   ├── hashring.py
│   └── *init*.py
│
├── docker-compose.yml      # Orchestrates server containers
├── Dockerfile              # Dockerfile for load balancer
├── requirements.txt        # Python dependencies for load balancer
└── .gitignore              # Ignores venv, pycache, etc.

`

---

⚙ Features

- ✅ Custom Consistent Hash Ring
- ✅ Virtual Server Support
- ✅ Quadratic Probing for Conflict Resolution
- ✅ Dockerized Server Containers
- ✅ Fault Detection & Auto Recovery
- ✅ Scalability Testing
- ✅ Visual Analysis with Plots

---

🚀 Getting Started

 1. Clone the Repository

bash
git clone https://github.com/your-username/LoadBalancerProject.git
cd LoadBalancerProject
`

2. Set Up Virtual Environment

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


3. Build Docker Containers

Make sure Docker is running:

bash
docker-compose up --build


---

📊 Running Analysis Tasks

Each analysis task demonstrates a concept:

| Task | Script          | Description                                     |
| ---- | --------------- | ----------------------------------------------- |
| A1   | `analyze_a1.py` | Verifies basic load distribution                |
| A2   | `analyze_a2.py` | Tests scalability with different replica counts |
| A3   | `analyze_a3.py` | Simulates server failure and recovery           |

Run using:

bash
python3 analysis/analyze_a1.py
python3 analysis/analyze_a2.py
python3 analysis/analyze_a3.py


---

📦 Server Container

Each server is a Flask app that responds to `GET /` with a simple message. Containers are spawned dynamically using `docker-compose.yml`.

---

🔁 Load Balancer Logic

The load balancer:

* Maps requests to servers using a custom hash function.
* Detects when a server is unresponsive.
* Removes and restarts failed servers.
* Ensures virtual server mapping for even distribution.

---

📌 Hashing Strategy

* Hash Ring Size**: 512 slots
* Virtual Servers per Container: 9
* Request Hashing: `H(i) = i + 2i + 17 mod 512`
* Virtual Server Hashing: `Φ(i,j) = i + j + 2j + 25 mod 512`
* Collision Handling: Quadratic Probing

---

✅ To-Do for First-Time Users

* [ ] Install Docker
* [ ] Install Python 3.8+
* [ ] Activate virtualenv
* [ ] Run `docker-compose up`
* [ ] Run analysis scripts from the `/analysis` folder

---

🙋‍♂ Contributions & Issues

Feel free to fork, improve, and raise issues if you find bugs or have ideas. This project is for educational purposes and welcomes collaboration.

---

📄 License

This project is under the MIT License.

---

✨ Acknowledgements

This project was developed as part of a systems lab to demonstrate consistent hashing, fault tolerance, and scalable service design using Python and Docker.
