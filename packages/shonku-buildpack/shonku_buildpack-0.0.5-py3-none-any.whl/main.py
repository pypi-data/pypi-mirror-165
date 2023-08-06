from buildpack import Buildpack
bp = Buildpack(f"myapp")
if __name__ == "__main__":
    bp.generateDockerfile("./Shonkufile", ".", 4000)