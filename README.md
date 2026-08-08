# VSCode ROS2 Workspace Template

This template will get you set up using ROS2 with VSCode as your IDE.

The development environment is set up using a VSCode devcontainer, and the same configuration is also used in CI.

## Features

### Development environment

The devcontainer uses the Microsoft Ubuntu devcontainer image along with the ROS2 devcontainer feature.

If you want to change which version of ROS you're using, update the ROS2 feature in `.devcontainer/devcontainer.json`:

```jsonc id="vozthd"
"ghcr.io/althack/devcontainers/ros2:0": {
  "distro": "lyrical",
  "package": "desktop"
}
```

This is also the ROS version used in CI, so you only need to change it in one place.

### Style

ROS2-approved formatters are included in the IDE.

* **c++** uncrustify; config from `ament_uncrustify`
* **python** autopep8; vscode settings consistent with the [style guide](https://docs.ros.org/en/lyrical/The-ROS2-Project/Contributing/Code-Style-Language-Versions.html)

### Tasks

There are many pre-defined tasks, see [`.vscode/tasks.json`](.vscode/tasks.json) for a complete listing. Feel free to adjust them to suit your needs.

Take a look at [how I develop using tasks](https://www.allisonthackston.com/articles/vscode_tasks.html) for an idea of how I use tasks in my development.

### Debugging

This template sets up debugging for python files, gdb for cpp programs, and ROS launch files.

See [`.vscode/launch.json`](.vscode/launch.json) for configuration details.

### Continuous Integration

The template also comes with basic continuous integration set up. See [`.github/workflows/ros.yaml`](.github/workflows/ros.yaml).

The build, test, and lint jobs run using the same devcontainer configuration used for development. This means changing the ROS distro in `.devcontainer/devcontainer.json` also changes the version used by CI.

To remove a linter, just delete its name from the matrix:

```yaml id="nxevf7"
matrix:
  linter:
    - cppcheck
    - cpplint
    - uncrustify
    - lint_cmake
    - xmllint
    - flake8
    - pep257
```

## How to use this template

### Prerequisites

You should already have Docker and VSCode with the Dev Containers extension installed on your system.

* [docker](https://docs.docker.com/engine/install/)
* [vscode](https://code.visualstudio.com/)
* [vscode dev containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

If you're using Windows, I recommend using WSL2 and opening the repository from your WSL distro before reopening it in the container.

### Get the template

Click on **Use this template**.

![template_use](https://user-images.githubusercontent.com/6098197/91331899-43f23b80-e780-11ea-92c8-b4665ce126f1.png)

### Create your repository

On the next dialog, name the repository you would like to start and choose its visibility.

![template_new](https://user-images.githubusercontent.com/6098197/91332035-713ee980-e780-11ea-81d3-13b170f568b0.png)

Github will then create a new repository with the contents of this one in your account. It grabs the latest changes as the initial commit.

### Clone your repo

Now you can clone your repo as normal.

![template_download](https://user-images.githubusercontent.com/6098197/91332342-e4e0f680-e780-11ea-9525-49b0afa0e4bb.png)

### Open it in vscode

Now that you've cloned your repo onto your computer, open it in VSCode (`File -> Open Folder`).

When you open it for the first time, you should see a popup asking if you would like to reopen it in a container. Say yes!

![template_vscode](https://user-images.githubusercontent.com/6098197/91332551-36898100-e781-11ea-9080-729964373719.png)

If you don't see the popup, open the command palette and select:

```text id="fipghb"
Dev Containers: Reopen in Container
```

VSCode will set up the container from `.devcontainer/devcontainer.json`, install ROS2 and the configured development tools, and install the recommended VSCode extensions.

Once that's finished, open a terminal inside VSCode and you're ready to go.

## Update the template with your code

1. Specify the repositories you want to include in your workspace in `src/ros2.repos`, or delete `src/ros2.repos` and develop directly within the workspace.
2. If you are using a `ros2.repos` file, import the contents with `Terminal -> Run Task... -> import from workspace file`.
3. Install dependencies with `Terminal -> Run Task... -> install dependencies`.
4. Adjust the scripts to your liking. These scripts are used both within tasks and CI.

   * `setup.sh` - setup commands for your code. By default this imports the workspace and installs dependencies.
   * `build.sh` - build commands for your code. By default this uses `--merge-install` and `--symlink-install`.
   * `test.sh` - test commands for your code.
5. Develop!

## Changing the ROS distro

The ROS distro is selected by the ROS2 feature in `.devcontainer/devcontainer.json`:

```jsonc id="si9pp5"
"ghcr.io/althack/devcontainers/ros2:0": {
  "distro": "lyrical",
  "package": "desktop"
}
```

Change `distro` to the version you want to use and rebuild the container.

Since CI uses the same devcontainer configuration, you don't need to update the ROS distro anywhere else.

## GUI applications

### Windows / WSL2

If you're using Windows, open the repository from your WSL2 distro and then reopen it in the devcontainer.

Current versions of VSCode Dev Containers and WSLg handle the display forwarding for you, so you shouldn't need to manually configure `DISPLAY`, Wayland, PulseAudio, or `/mnt/wslg` mounts.

### Linux / X11

If you're using native Linux with X11, uncomment the X11 forwarding feature in `.devcontainer/devcontainer.json`:

```jsonc id="mxugk2"
"ghcr.io/althack/devcontainers/linux-x11-forwarding:0": {},
```

Some GUI applications may also need the container to share the host IPC namespace. If you run into rendering problems, try uncommenting:

```jsonc id="9b5wt2"
"--ipc=host"
```

in `runArgs`.

## NVIDIA / CUDA

CUDA support is optional.

If you want to use CUDA, uncomment the NVIDIA CUDA feature in `.devcontainer/devcontainer.json`:

```jsonc id="w72s2s"
"ghcr.io/devcontainers/features/nvidia-cuda:3": {
  "installToolkit": true
}
```

and allow the container to access the host GPU:

```jsonc id="xa78sc"
"--gpus",
"all"
```

You'll also need working NVIDIA drivers and the NVIDIA Container Toolkit installed on the host.

See the [NVIDIA Container Toolkit installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for setup instructions.

I don't test all of the possible NVIDIA/CUDA host configurations, so your mileage may vary here.

## Repos are not showing up in VS Code source control

VSCode doesn't necessarily know about repositories you've imported underneath the workspace.

You can add them directly using:

```text id="jwb7ls"
File -> Add Folder To Workspace
```

![Screenshot-26](https://github.com/althack/vscode_ros2_workspace/assets/6098197/d8711320-2c16-463b-9d67-5bd9314acc7f)

Or you can add them as git submodules.

![Screenshot-27](https://github.com/althack/vscode_ros2_workspace/assets/6098197/8ebc9aac-9d70-4b53-aa52-9b5b108dc935)

To add all of the repos in your `*.repos` file as submodules, run:

```bash id="1pnpb2"
python3 .devcontainer/repos_to_submodules.py
```

or run the task titled:

```text id="7do355"
add submodules from .repos
```
