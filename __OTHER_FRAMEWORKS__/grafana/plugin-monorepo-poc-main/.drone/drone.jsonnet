local plugins = std.split(std.extVar('plugins'), ' ');

local images = {
  node: 'node:16',
  golang: 'golang:1.17.6',
  golangci_lint: 'golangci/golangci-lint:v1.44.0',
  jsonnet_build: 'grafana/jsonnet-build:c8b75df',
};

local step(name, commands, image, env) = {
  name: name,
  commands: commands,
  image: image,
  environment+: {
    PLUGIN: env
  },
};

local pipeline(name, steps=[]) = {
  kind: 'pipeline',
  type: 'docker',
  name: name,
  environment+: {
    PLUGIN: name
  },
  steps: steps,
  image_pull_secrets: ['dockerconfigjson'],
  trigger+: {
    ref+: [
      'refs/pull/**',
      'refs/heads/main',
    ],
    paths: 'plugins/' + name + "/*",
  },
};

[
  pipeline(p, [
    step(
        'build',
        ['cd ./plugins/' + p, 'yarn install', 'yarn build'],
        images.node,
        p
      )
  ]) for p in plugins
]