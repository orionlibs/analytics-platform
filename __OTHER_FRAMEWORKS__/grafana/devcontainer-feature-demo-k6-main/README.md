# devcontainer-feature-demo-k6

**Example repository to demonstrate the use of the [k6 Dev Container feature](https://github.com/grafana/devcontainer-features/tree/main/src/k6)**

This repository contains a k6 example script created by the `k6 new` command. The k6 test script can be run in the [Dev Container](https://containers.dev) using the following command:

```bash
k6 run script.js
```

## Usage

The repository contains a [Development Container](https://containers.dev/) configuration, which means that k6 tests can be run immediately, without installing k6, in any [environment that supports Dev Containers](https://containers.dev/supporting) (GitHub Codespaces, JetBrains IDEs, Visual Studio Code, DevPods, CodeSandbox, etc)

**Without installing software**

You can *run k6 test without installing any software* using [GitHub Codespaces](https://docs.github.com/en/codespaces). After [forking this](https://github.com/grafana/devcontainer-feature-demo-k6/fork) repository, [create a codespace for your repository](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository).

The created codespace will contain the k6 executable so that the test can be run immediately in a terminal window:

```bash
k6 run script.js
```

**Using an IDE**

You can run k6 test using [Visual Studio Code](https://code.visualstudio.com/) if the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension is installed. After [forking this repository](https://github.com/grafana/devcontainer-feature-demo-k6/fork), clone your repository and open the folder with Visual Studio Code. It will automatically detect that the folder contains a Dev Container configuration and ask you whether to open the folder in a container. Choose **"Reopen in Container"**.

After reopening in the Dev Container, the test script can be run immediately in the terminal window:

```bash
k6 run script.js
```

## Configuration

The Dev Container configuration is in the `.devcontainer/devcontainer.json` file:

```json file=.devcontainer/devcontainer.json
{
  "name": "devcontainer-feature-demo-k6",
  "image": "mcr.microsoft.com/devcontainers/base:0-alpine",
  "features": {
    "ghcr.io/grafana/devcontainer-features/k6:1": {}
  }
}
```

This is the minimal Dev Container configuration for using k6. In addition to the container name and the Alpine base image reference, it only contains the k6 Dev Container feature reference.
