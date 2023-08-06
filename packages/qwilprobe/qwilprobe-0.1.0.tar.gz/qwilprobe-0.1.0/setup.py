from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

def generate_grpc():
    print("Generating grpc code...")
    import grpc_tools.protoc

    grpc_tools.protoc.main([
        "grpc_tools.protoc",
        "--proto_path=proto/",
        "--python_out=src/qwilprobe/generated",
        "--grpc_python_out=src/qwilprobe/generated",
        "qwilprobe.proto"
    ])

def fix_import_path():
    print("Fixing import path in generated grpc code...")
    filename = 'src/qwilprobe/generated/qwilprobe_pb2_grpc.py'
    with open(filename) as infile:
        lines = infile.read()
    lines = lines.replace('import qwilprobe_pb2 as qwilprobe__pb2',
                          'import qwilprobe.generated.qwilprobe_pb2 as qwilprobe__pb2')

    with open(filename, 'w') as outfile:
        for line in lines:
            outfile.write(line)

class BuildPyWithGrpcGeneration(build_py):
    def run(self):
        generate_grpc()
        fix_import_path()
        super(BuildPyWithGrpcGeneration, self).run()

class DevelopWithGrpcGeneration(develop):
    def run(self):
        generate_grpc()
        fix_import_path()
        super(DevelopWithGrpcGeneration, self).run()

setup(cmdclass={"build_py": BuildPyWithGrpcGeneration,
                "develop": DevelopWithGrpcGeneration})
