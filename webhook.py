from flask import Flask, request
import os
#test
app = Flask(__name__)

@app.route("/git-update", methods=["POST"])
def git_update():
    if request.method == "POST":
        os.system("cd /home/ec2-user/Fc-Tryhard-bot && git pull")
        return "Git Pull effectué", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)