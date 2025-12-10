# devcontainer-feature-demo-xk6

**Example repository to demonstrate the use of the [xk6 Dev Container feature](https://github.com/grafana/devcontainer-features/tree/main/src/xk6)**

This repository contains a k6 example extension that implements base32 encoding. The k6 test script can be run in the [Dev Container](https://containers.dev) using the following command:

```bash
xk6 run script.js
```

k6 with the example extension can be built using the following command:

```bash
xk6 build --with github.com/grafana/devcontainer-feature-demo-xk6=.
```

After that, the test script can be run with the built k6 as follows:

```bash
./k6 run script.js
```

The API documentation can be generated using the following command:

```bash
npx -y typedoc
```

The above command generates the API documentation from the `index.d.ts` file into the `build/docs` directory.

## Usage

The repository contains a [Development Container](https://containers.dev/) configuration, which means that k6 tests can be run immediately, without installing k6, in any [environment that supports Dev Containers](https://containers.dev/supporting) (GitHub Codespaces, JetBrains IDEs, Visual Studio Code, DevPods, CodeSandbox, etc)

**Without installing software**

You can *build k6 extension without installing any software* using [GitHub Codespaces](https://docs.github.com/en/codespaces). After [forking this](https://github.com/grafana/devcontainer-feature-demo-xk6/fork) repository, [create a codespace for your repository](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository).

The created codespace will contain the xk6 executable and the go toolkit so that the test script can be run with example extension immediately in a terminal window:

```bash
xk6 run script.js
```

**Using an IDE**

You can run k6 test using [Visual Studio Code](https://code.visualstudio.com/) if the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension is installed. After [forking this repository](https://github.com/grafana/devcontainer-feature-demo-xk6/fork), clone your repository and open the folder with Visual Studio Code. It will automatically detect that the folder contains a Dev Container configuration and ask you whether to open the folder in a container. Choose **"Reopen in Container"**.

After reopening in the Dev Container, the test script can be run with extension immediately in the terminal window:

```bash
xk6 run script.js
```

## Configuration

The Dev Container configuration is in the `.devcontainer/devcontainer.json` file:

```json file=.devcontainer/devcontainer.json
{
  "name": "devcontainer-feature-demo-xk6",
  "image": "mcr.microsoft.com/devcontainers/base:1-bookworm",

  "features": {
    "ghcr.io/devcontainers/features/go:1": {
      "version": "1.23",
      "golangciLintVersion": "1.63.4"
    },
    "ghcr.io/grafana/devcontainer-features/xk6:1": { "version": "0.14.0" },
    "ghcr.io/devcontainers/features/node:1": { "version": "22" }
  }
}
```

This is a relatively minimal Dev Container configuration for developing k6 extensions. In addition to the container name and the Debian base image reference, it only contains the following Dev Container feature references:

- **go** the latest `1.23.x` version of the go toolkit with `golangci-lint` version `1.63.4`.
- **xk6** the `xk6` tool version `0.14.0`.
- **node** Node.js version `22` for generating documentation with [TypeDoc](https://typedoc.org/).
