# VSCode ROS2 Workspace Template

This template will get you set up using ROS2 with VSCode as your IDE.

See [how I develop with vscode and ros2](https://www.allisonthackston.com/articles/vscode_docker_ros2.html) for a more in-depth look on how to use this workspace.

## Features

### Style

ROS2-approved formatters are included in the IDE.  

* **c++** uncrustify; config from `ament_uncrustify`
* **python** autopep8; vscode settings consistent with the [style guide](https://docs.ros.org/en/lyrical/The-ROS2-Project/Contributing/Code-Style-Language-Versions.html)

### Tasks

There are many pre-defined tasks, see [`.vscode/tasks.json`](.vscode/tasks.json) for a complete listing.  Feel free to adjust them to suit your needs.  

Take a look at [how I develop using tasks](https://www.allisonthackston.com/articles/vscode_tasks.html) for an idea on how I use tasks in my development.

### Debugging

This template sets up debugging for python files, gdb for cpp programs and ROS launch files.  See [`.vscode/launch.json`](.vscode/launch.json) for configuration details.

### Continuous Integration

The template also comes with basic continuous integration set up. See [`.github/workflows/ros.yaml`](/.github/workflows/ros.yaml).

To remove a linter just delete it's name from this line:

```yaml
      matrix:
          linter: [cppcheck, cpplint, uncrustify, lint_cmake, xmllint, flake8, pep257]
```

## How to use this template

### Prerequisites

You should already have Docker and VSCode with the remote containers plugin installed on your system.

* [docker](https://docs.docker.com/engine/install/)
* [vscode](https://code.visualstudio.com/)
* [vscode remote containers plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### NVidia support

To make nvidia driver and opengl available in docker, follow the installation instructions for docker-nvidia.
They include the steps in docker and add the additional gpu layer.

* [docker-nvidia (includes docker install and additional installation for NVidia GPU accelerated hosts)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

### Get the template

Click on "use this template"

![template_use](https://user-images.githubusercontent.com/6098197/91331899-43f23b80-e780-11ea-92c8-b4665ce126f1.png)

### Create your repository

On the next dialog, name the repository you would like to start and decide if you want all of the branches, or the default branch.

> [!IMPORTANT]
> 
> The new default branch supports any version of ROS by setting the appropriate version you want in the 'FROM' line in `.devcontainer/Dockerfile`
>
> By default, this is set to `althack/ros2:lyrical-full`

![template_new](https://user-images.githubusercontent.com/6098197/91332035-713ee980-e780-11ea-81d3-13b170f568b0.png)

Github will then create a new repository with the contents of this one in your account.  It grabs the latest changes as "initial commit".

### Clone your repo

Now you can clone your repo as normal

![template_download](https://user-images.githubusercontent.com/6098197/91332342-e4e0f680-e780-11ea-9525-49b0afa0e4bb.png)

### Open it in vscode

Now that you've cloned your repo onto your computer, you can open it in VSCode (File->Open Folder).

When you open it for the first time, you should see a little popup that asks you if you would like to open it in a container.  Say yes!

![template_vscode](https://user-images.githubusercontent.com/6098197/91332551-36898100-e781-11ea-9080-729964373719.png)

If you don't see the pop-up, click on the little green square in the bottom left corner, which should bring up the container dialog

![template_vscode_bottom](https://user-images.githubusercontent.com/6098197/91332638-5d47b780-e781-11ea-9fb6-4d134dbfc464.png)

In the dialog, select "Remote Containers: Reopen in container"

VSCode will build the dockerfile inside of `.devcontainer` for you.  If you open a terminal inside VSCode (Terminal->New Terminal), you should see that your username has been changed to `ros`, and the bottom left green corner should say "Dev Container"

![template_container](https://user-images.githubusercontent.com/6098197/91332895-adbf1500-e781-11ea-8afc-7a22a5340d4a.png)

### Update the template with your code

1. Specify the repositories you want to include in your workspace in `src/ros2.repos` or delete `src/ros2.repos` and develop directly within the workspace.
2. If you are using a `ros2.repos` file, import the contents `Terminal->Run Task..->import from workspace file`
3. Install dependencies `Terminal->Run Task..->install dependencies`
4. (optional) Adjust scripts to your liking.  These scripts are used both within tasks and CI.
   * `setup.sh` The setup commands for your code.  Default to import workspace and install dependencies.
   * `build.sh` The build commands for your code.  Default to `--merge-install` and `--symlink-install`
   * `test.sh` The test commands for your code.
5. Develop!

## FAQ

### XAuthority

If you see the error:

```text
Authorization required, but no authorization protocol specified Unable to open display: :0 Authorization required, but no authorization protocol specified
```

You may need to update the UID/GID to match yours.  In `.devcontainer/devcontainer.json` update the lines that are marked `Change to match your UID` and `Change to match your GID`

.devcontainer/devcontainer.json

```jsonc
 "build": {
  "args": {
   ...
   // "USERNAME": "ros",
   // "USER_UID": "1000", //Change to match your UID
   // "USER_GID": "1000" // Change to match your GID
  },
 },
 ...
 "runArgs": [
  ...
  "--volume=/run/user/1000:/run/user/1000", // Change 1000 to match your UID
  ...
 ],
```

### XDisplay

If you see the error:

```text
Couldn't open X display in GLXGLSupport::getGLDisplay at ./.obj-x86_64-linux-gnu/ogre_vendor-prefix/src/ogre_vendor/RenderSystems/GLSupport/src/GLX/OgreGLXGLSupport.cpp
```

You need to remove or comment out the wayland options

```jsonc
 "runArgs": [
  ...
  // Wayland host
  //"--volume=/mnt/wslg:/mnt/wslg",
  // "--volume=/run/user/1000:/run/user/1000",
  // uncomment to use intel iGPU
  // "--device=/dev/dri"
  ...
 ],
 ...
  "containerEnv": {
  ...
  // For Wayland
  // "WAYLAND_DISPLAY": "${localEnv:WAYLAND_DISPLAY}",
  // "XDG_RUNTIME_DIR": "${localEnv:XDG_RUNTIME_DIR}",
  // "QT_QPA_PLATFORM": "wayland", // Force Wayland
  ...
 },
```

### WSL2

#### The gui doesn't show up

This is likely because the DISPLAY environment variable is not getting set properly.

1. Find out what your DISPLAY variable should be

      In your WSL2 Ubuntu instance

      ```bash
      echo $DISPLAY
      ```

2. Copy that value into the `.devcontainer/devcontainer.json` file

      ```jsonc
      "containerEnv": {
        "DISPLAY": ":0",
      }
      ```

#### I want to use vGPU

If you want to access the vGPU through WSL2, you'll need to add additional components to the `.devcontainer/devcontainer.json` file in accordance to [these directions](https://github.com/microsoft/wslg/blob/main/samples/container/Containers.md)

```jsonc
 "runArgs": [
  "--network=host",
  "--cap-add=SYS_PTRACE",
  "--security-opt=seccomp:unconfined",
  "--security-opt=apparmor:unconfined",
  "--volume=/tmp/.X11-unix:/tmp/.X11-unix",
  "--volume=/mnt/wslg:/mnt/wslg",
  "--volume=/usr/lib/wsl:/usr/lib/wsl",
  "--device=/dev/dxg",
  "--gpus=all"
 ],
 "containerEnv": {
  "DISPLAY": "${localEnv:DISPLAY}", // Needed for GUI try ":0" for windows
  "WAYLAND_DISPLAY": "${localEnv:WAYLAND_DISPLAY}",
  "XDG_RUNTIME_DIR": "${localEnv:XDG_RUNTIME_DIR}",
  "PULSE_SERVER": "${localEnv:PULSE_SERVER}",
  "LD_LIBRARY_PATH": "/usr/lib/wsl/lib",
  "LIBGL_ALWAYS_SOFTWARE": "1" // Needed for software rendering of opengl
 },
```

### Repos are not showing up in VS Code source control

This is likely because vscode doesn't necessarily know about other repositories unless you've added them directly.

```text
File->Add Folder To Workspace
```

![Screenshot-26](https://github.com/althack/vscode_ros2_workspace/assets/6098197/d8711320-2c16-463b-9d67-5bd9314acc7f)

Or you've added them as a git submodule.

![Screenshot-27](https://github.com/althack/vscode_ros2_workspace/assets/6098197/8ebc9aac-9d70-4b53-aa52-9b5b108dc935)

To add all of the repos in your *.repos file, run the script

```bash
python3 .devcontainer/repos_to_submodules.py
```

or run the task titled `add submodules from .repos`

### Error handling for GPU acceleration

#### Docker image cannot be built:

The dockerfile can be built but using devcontainer.json results in error messages like "docker container cannot connect to device [[gpu]]" means docker itself is installed, but not the above mentioned nvidia part.

Solution is, to follow the guide and the test with nvidia-smi as indicated here:

- [docker-nvidia(for GPU acceleration on Nvidia GPU hosts)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

#### Programs in Docker cannot access GPU

Error messages that show lacking GPU acceleration (in docker terminal)

```bash
sudo apt-get update   && sudo apt-get install -y -qq glmark2   && glmark2
```

results in:

```bash
   libGL error: No matching fbConfigs or visuals found
   libGL error: failed to load driver: swrast
      X Error of failed request:  GLXBadContext
   Major opcode of failed request:  151 (GLX)
   Minor opcode of failed request:  6 (X_GLXIsDirect)
   Serial number of failed request:  48
   Current serial number in output stream:  47
```

Solution is, to follow the guide and the test with nvidia-smi as indicated here: 
[docker-nvidia(for GPU acceleration on Nvidia GPU hosts)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

#### more information

https://wiki.ros.org/docker/Tutorials/GUI
https://medium.com/@benjamin.botto/opengl-and-cuda-applications-in-docker-af0eece000f1
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
