# Ironclad Selectors

Ironclad Selectors is a small, injectable code snippet for a browser environment that is designed to traverse the DOM tree when elements are clicked and create selectors that are as strong and endurable as possible.

The current version currently only generates xpath selectors but future versions will support various selector types compatible with different frameworks.

## Installation

Include `dist/index.js` in your project. You can build a minified version by running `yarn build`.

## Development

There is a watch script for development: `yarn watch`. As this is a pre-alpha version it is currently being combined with utilizing an external live server (such as VSCode extension [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)) to develop against.

## Why?

This project is designed to act as a separate and maintainable library for generating strong DOM selectors that are decoupled from any existing project. The main motivation for creating this package is to ensure projects such as [Playback Singers](https://github.com/grafana/hackathon-2024-03-playback-singers/tree/main/packages/chrome-extension/src/replay/features) create selectors that are as strong and resistant to change as possible, ensuring users with less technical knowledge can create and maintain tests utilizing best practice.

## Is this like Playwright's selector engine?

Possibly! I found out about Playwright's selector engine after I started this project. I was hoping they had utilized an external library for generating selectors but they have created their own [which is tightly coupled with their implementation](https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/injected/selectorGenerator.ts).
