from flask import Flask, request, jsonify
import docker
import time
from .hashring import ConsistentHashRing

app = Flask(__name__)
client = docker.from_env()

ring = ConsistentHashRing()
containers = {}

@app.route("/rep")
def replicas():
    return jsonify({"status": "successful", "message": ring.describe()})

@app.route("/add", methods=["POST"])
def add_servers():
    data = request.get_json()
    hostnames = data.get("hostnames", [])

    for name in hostnames:
        try:
            # Remove container if already exists but is exited or dead
            try:
                existing = client.containers.get(name)
                if existing.status != "running":
                    existing.remove(force=True)
            except docker.errors.NotFound:
                pass

            container = client.containers.run(
                "server_image",
                name=name,
                detach=True,
                network="load_balancer_project_net1",
                hostname=name
            )
            time.sleep(1)
            ring.add_server(name)
            containers[name] = container
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})

    return jsonify({"status": "successful", "message": ring.describe()})

@app.route("/rm", methods=["POST"])
def remove_server():
    data = request.get_json()
    hostname = data.get("hostname")

    if hostname in containers:
        container = containers[hostname]
        container.stop()
        container.remove()
        del containers[hostname]
        ring.remove_server(hostname)
        return jsonify({"status": "successful", "message": ring.describe()})
    else:
        return jsonify({"status": "failure", "message": "Server not found"})

@app.route("/home")
def route_home():
    import random
    request_id = random.randint(1, 10000)
    server = ring.get_server(request_id)

    if server:
        try:
            container = client.containers.get(server)
            if container.status != "running":
                raise Exception("Container not running")

            res = container.exec_run("curl -s http://localhost:5000/")
            return jsonify({
                "status": "successful",
                "server": server,
                "response": res.output.decode()
            })
        except Exception as e:
            print(f"[!] Detected failure in {server}: {e}. Attempting recovery...")

            try:
                # Attempt to remove existing container if it's corrupt
                try:
                    container = client.containers.get(server)
                    container.remove(force=True)
                    print(f"[-] Removed failed container: {server}")
                except docker.errors.NotFound:
                    print(f"[!] Container {server} not found, safe to recreate.")

                # Recreate container with same name
                new_container = client.containers.run(
                    "server_image",
                    name=server,
                    detach=True,
                    network="load_balancer_project_net1",
                    hostname=server
                )
                containers[server] = new_container

                # Ensure it's in the hash ring
                if server not in ring.servers:
                    ring.add_server(server)

                print(f"[+] Recovered and restarted server: {server}")

                return jsonify({
                    "status": "recovered",
                    "server": server,
                    "response": "",
                    "message": f"{server} was down and restarted"
                })
            except Exception as inner_e:
                return jsonify({
                    "status": "failure",
                    "message": f"Failed to recover {server}: {str(inner_e)}"
                })
    else:
        return jsonify({"status": "failure", "message": "<Error> No server available"})

@app.route("/clear", methods=["POST"])
def clear():
    try:
        for container in client.containers.list(all=True):
            if container.name.startswith("S"):
                print(f"Removing container: {container.name}")
                container.remove(force=True)

        ring.clear()
        containers.clear()

        return jsonify({
            "message": "All server replicas cleared.",
            "status": "successful"
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "failure"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
