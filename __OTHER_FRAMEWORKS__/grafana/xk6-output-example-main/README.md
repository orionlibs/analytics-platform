# xk6-output-example

**Example k6 output extension**

This k6 extension showcases how to develop a k6 Output extension. It serves as the basis for new Output extensions created with the `xk6 new` command. Additionally, this repository functions as a GitHub template for creating k6 output extension repositories.

**script.sh**
```shell file=script.sh
XK6_EXAMPLE_INTERVAL=10s ./k6 run -o example=script.csv script.js
```

**script.js**
```javascript file=script.js
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: "constant-vus",
      vus: 2,
      duration: "30s",
    },
  },
};

export default function () {
  http.get('https://quickpizza.grafana.com');

  sleep(.5);
}
```

## Quick start

1. **Create a GitHub repository**. This can be done interactively in a browser by clicking [here](https://github.com/new?template_name=xk6-output-example&template_owner=grafana).

    Alternatively, use the [GitHub CLI](https://cli.github.com/) to create the repository.

    ```shell
   gh repo create -p grafana/xk6-output-example -d "Experimental k6 output extension" --public xk6-output-quickstart
    ```

2. **Create a codespace**. Go to the repository you created in the previous step. Click the green **Code** button and then select **Codespaces** from the dropdown menu. Click **Create new codespace**.

    Alternatively, use the [GitHub CLI](https://cli.github.com/) to create the codespace, replacing `USER` with your GitHub username:

    ```shell
    gh codespace create --repo USER/xk6-output-quickstart --web
    ```

    Once the codespace is ready, it will open in your browser as a Visual Studio Code-like environment, letting you begin working on your project with the repository code already checked out.

3. Run the test script. The repository's root directory includes a `script.js` file. When developing k6 extensions, use the `xk6 run` command instead of `k6 run` to execute your scripts.

    ```shell
    xk6 run -- --out quickstart script.js
    ```

## Development environment

While using a GitHub codespace in the browser is a good starting point, you can also set up a local development environment for a better developer experience.

To create a local development environment, you need an IDE that supports [Development Containers](https://containers.dev/). [Visual Studio Code](https://code.visualstudio.com/) supports Development Containers after installing the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

1. First, clone the `xk6-output-quickstart` repository to your machine and open it in Visual Studio Code. Make sure to replace `USER` with your GitHub username:

   ```shell
   git clone https://github.com/USER/xk6-output-quickstart.git
   code xk6-output-quickstart
   ```

2. Visual Studio Code will detect the [development container](https://containers.dev/) configuration and show a pop-up to open the project in a dev container. Accept the prompt and the project opens in the dev container, and the container image is rebuilt if necessary.

3. Run the test script. The repository's root directory includes a `script.js` file. When developing k6 extensions, use the `xk6 run` command instead of `k6 run` to execute your scripts.

    ```shell
    xk6 run -- --out quickstart script.js
    ```

## Starter

The repository demonstrates how to handle metrics. These files are useful as a learning resource, but are not needed when creating a new extension.

You can use the `.starter.patch` file with the `git apply` command to delete these files.

```bash
git apply .starter.patch
rm .starter.patch
```

## Download

Building a custom k6 binary with the `xk6-output-example` extension is necessary for its use. You can download pre-built k6 binaries from the [Releases page](https://github.com/grafana/xk6-output-example/releases/).

## Build

Use the [xk6](https://github.com/grafana/xk6) tool to build a custom k6 binary with the `xk6-output-example` extension. Refer to the [xk6 documentation](https://github.com/grafana/xk6) for more information.

## Contribute

If you wish to contribute to this project, please start by reading the [Contributing Guidelines](http://CONTRIBUTING.md).

