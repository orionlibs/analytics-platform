/* eslint-disable @typescript-eslint/no-explicit-any */
console.log("Hello, index!");

const output = document.getElementById("output")!;

function log(name: string, message: unknown) {
  const asString =
    typeof message === "string" ? message : JSON.stringify(message, null, 2);
  output.innerHTML += `${name}: ${asString}\n`;
}

async function main() {
  //
  // screen size
  try {
    const innerSize = {
      width: window.innerWidth,
      height: window.innerHeight,
    };

    log("inner size", JSON.stringify(innerSize));

    const screenSize = {
      width: window.screen.width,
      height: window.screen.height,
    };

    log("screen client size", JSON.stringify(screenSize));
  } catch (error: any) {
    const message = error?.message ?? error?.toString?.() ?? "unknown error";
    log("screen size error", message);
  }

  //
  // hardware concurrency
  try {
    log("hardware concurrency", window.navigator.hardwareConcurrency);
  } catch (error: any) {
    const message = error?.message ?? error?.toString?.() ?? "unknown error";
    log("hardware concurrency", message);
  }

  //
  // canvas webgl getContextAttributes
  try {
    const canvas = document.getElementById("canvas");

    if (!canvas || !(canvas instanceof HTMLCanvasElement)) {
      throw new Error("canvas not found");
    }

    const gl = canvas.getContext("webgl");

    if (!gl) {
      throw new Error("webgl context not found");
    }

    const attributes = gl.getContextAttributes();
    log("webgl canvas attributes", attributes ?? "no attributes");
  } catch (error: any) {
    const message = error?.message ?? error?.toString?.() ?? "unknown error";
    log("webgl canvas", message);
  }

  //
  // webgpu requestAdapter
  try {
    if (!navigator.gpu) {
      throw Error("WebGPU not supported.");
    }

    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
      throw Error("Couldn't request WebGPU adapter.");
    }

    const device = await adapter.requestDevice();

    const adapterInfo: GPUAdapterInfo | undefined = device.adapterInfo;
    const adapterInfoValues = adapterInfo && {
      architecture: adapterInfo.architecture,
      description: adapterInfo.description,
      device: adapterInfo.device,
      vendor: adapterInfo.vendor,
      subgroupMaxSize: adapterInfo.subgroupMaxSize,
      subgroupMinSize: adapterInfo.subgroupMinSize,
    };

    const adapterFeatures = Array.from(adapter.features.values());
    const deviceFeatures = Array.from(device.features.values());

    log("webgpu adapter", {
      adapterInfo: adapterInfoValues,
      isFallbackAdapter: adapter.isFallbackAdapter,
      label: device.label,
      adapterFeatures,
      deviceFeatures,
    });
  } catch (error: any) {
    const message = error?.message ?? error?.toString?.() ?? "unknown error";
    log("webgpu requestAdapter", message);
  }
}

main();
