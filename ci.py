import subprocess
import os
import platform

proj_path = os.path.dirname(os.path.realpath(__file__))

def clone_thirdparty():
    cmd_ggtest = [
        "git", "clone",
        "https://github.com/google/googletest.git",
        os.path.join(proj_path,"third_party/googletest")
    ]
    p = subprocess.Popen(cmd_ggtest)
    p.wait()
    cmd_glslang = [
        "git", "clone",
        "https://github.com/google/glslang.git",
        os.path.join(proj_path,"third_party/glslang")
    ]
    p = subprocess.Popen(cmd_glslang)
    p.wait()
    cmd_spvtool = [
        "git", "clone",
        "https://github.com/KhronosGroup/SPIRV-Tools.git",
        os.path.join(proj_path,"third_party/spirv-tools")
    ]
    p = subprocess.Popen(cmd_spvtool)
    p.wait()
    cmd_spvheader = [
        "git", "clone",
        "https://github.com/KhronosGroup/SPIRV-Headers.git",
        os.path.join(proj_path,"third_party/spirv-headers")
    ]
    p = subprocess.Popen(cmd_spvheader)
    p.wait()

def build():
    clone_thirdparty()

    ndk = os.path.join( '' if 'ANDROID_HOME' not in os.environ else os.environ['ANDROID_HOME'], 'ndk-bundle')
    if os.path.exists(ndk):
        print('Build Android....')
        cmd_gen = [
            "cmake", '-GNinja',
            "-H" + proj_path,
            "-B" + os.path.join(proj_path, "build"),
            '-DCMAKE_TOOLCHAIN_FILE=' + os.path.join(ndk, 'build/cmake/android.toolchain.cmake'),
            '-DANDROID_ABI=armeabi-v7a', 
            '-DANDROID_ARM_NEON=ON',
            '-DANDROID_PLATFORM=android-24',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DSHADERC_SKIP_TESTS=ON',
            '-DSHADERC_SKIP_INSTALL=OFF',
            '-DCMAKE_INSTALL_PREFIX='+os.path.join(proj_path, 'build', 'artifacts')
        ]
        p = subprocess.Popen(cmd_gen)
        p.wait()
        cmd_build = [ "ninja", '-C', os.path.join(proj_path, "build"), 'install' ]
        p = subprocess.Popen(cmd_build)
        p.wait()
    else:
        if platform.system() == "Darwin":
            cmd_gen = [
                "cmake", '-GXcode',
                "-H" + proj_path,
                "-B" + os.path.join(proj_path, "build"),
                '-DCMAKE_TOOLCHAIN_FILE=' + os.path.join(proj_path, 'ios.cmake'),
                '-DSHADERC_SKIP_TESTS=ON',
                '-DSHADERC_SKIP_INSTALL=OFF',
                '-DCMAKE_INSTALL_PREFIX='+os.path.join(proj_path, 'build', 'artifacts')
            ]
            p = subprocess.Popen(cmd_gen)
            p.wait()
        else:
            cmd_gen = [
                "cmake", '-GVisual Studio 15 2017 Win64',
                "-H" + proj_path,
                "-B" + os.path.join(proj_path, "build"),
                '-DSHADERC_SKIP_TESTS=ON',
                '-DSHADERC_SKIP_INSTALL=OFF',
                '-DCMAKE_INSTALL_PREFIX='+os.path.join(proj_path, 'build', 'artifacts')
            ]
            p = subprocess.Popen(cmd_gen)
            p.wait()
        cmd_build = [
            "cmake",
            "--build", os.path.join(proj_path, "build"),
            '--config', 'Release',
            '--target', 'Install'
        ]
        p = subprocess.Popen(cmd_build)
        p.wait()

build()