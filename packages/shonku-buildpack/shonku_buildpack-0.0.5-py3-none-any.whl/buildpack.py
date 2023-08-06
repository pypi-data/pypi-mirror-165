class Buildpack:
    def __init__(self, project):
        self.project = project

    def parseScript(self, shonkufile):
        file = open(shonkufile)
        lines = file.read().split("\n")
        script = ""
        '''
            For web
        '''
        for i in lines:
            split = i.split(" ", 1)
            if split[0] == "web:":
                script = split[1]
        return script

    def dockerfiles(self, entrypoint):
        python = f'''FROM python:3.9.5-slim-buster\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD {entrypoint}'''
        return python

    def dockercompose(self):
        python = f"version: '3.8'\nservices:\n    app:\n        container_name: {self.project}\n        image: {self.project}\n        restart: always\n        ports:\n            - [PORT]:8000"
        return python

    def generateDockerfile(self, file, save_location):
        script = self.parseScript(file)
        dockerfile = self.dockerfiles(script)
        dockercompose = self.dockercompose()
        file = open(f"{save_location}/Dockerfile", "w")
        with file as f:
            f.write(dockerfile)
        file = open(f"{save_location}/docker-compose.yml", "w")
        with file as f:
            f.write(dockercompose)

