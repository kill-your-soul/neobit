import os
from flask import Flask, jsonify, make_response, request
import docker

client = docker.from_env()
app = Flask(__name__)


@app.route("/containers", methods=["GET"])
def get_containers():
    containers = client.containers.list()
    containers_json = [{"id": container.id} for container in containers]
    return jsonify({"containers": containers_json})


@app.route("/container/<string:container_id>", methods=["GET"])
def get_container(container_id: str):
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        return make_response(jsonify({"error": "Container not found"}), 404)
    return jsonify(
        {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "port": container.ports,
        }
    )


@app.route("/config", methods=["POST"])
def create_config():
    print(request.files)
    file = request.files["file"]
    file.save("./configs/" + file.filename)
    return make_response(jsonify({"message": "Config created"}), 201)


@app.route("/configs", methods=["GET"])
def get_configs():
    configs = [file for file in os.listdir("./configs")]
    return jsonify({"configs": configs})


# create a new container with the given config and run the socks5 proxy server on the given port
@app.route("/container", methods=["POST"])
def create_container():
    config = request.json["config"]
    port = len(client.containers.list())
    try:
        image = client.images.build(path=".", dockerfile="Dockerfile", tag="socks5", nocache=True)
    except docker.errors.BuildError as e:
        print(e)
        return make_response(jsonify({"error": "Error building image"}), 400)
    container = client.containers.run(
        "socks5",
        detach=True,
        ports={"8128/tcp": 8000 + int(port)},
        cap_add=["NET_ADMIN"],
        devices=["/dev/net/tun:/dev/net/tun"],
        # command=["openvpn", "--config " + config]
    )

    container.exec_run(
        "iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE", detach=True
    )
    container.exec_run(
        "openvpn --config "+ config, detach=True
    )
    return make_response(jsonify({"message": "Container created"}), 201)


if __name__ == "__main__":
    app.run(debug=True)
