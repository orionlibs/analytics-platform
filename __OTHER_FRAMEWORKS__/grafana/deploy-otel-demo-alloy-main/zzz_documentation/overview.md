## Summary
This is a project that you can use to quickly and easily deploy [Grafana Alloy](https://grafana.com/docs/alloy/latest/) as an OpenTelemetry collector for the [OpenTelemetry Demo](https://opentelemetry.io/docs/demo/architecture/).

A few points to mention:
- The OTel Demo is deployed only with its microservices (e.g. without the O11y stack shown in the architecture link above);
- Grafana Alloy is deployed in place of the demo's OTel Collector;
- Alloy is configured to ship all the OTel Demo's OTLP-based telemetry to the Grafana Cloud instance of your choice.

<br>
<br>

## Goals and Technologies

### Reference example

The primary goal of this project is to provide a simple reference example of a set of microservices sending Open Telemetry to Grafana Cloud. If you have not gone through this before, it can be challenging at first to correctly configure all the connected parts; this project shows one way to do this quickly and easily. 

Specifically: there are a few setup steps (preparing your Grafana Cloud credentials for example) but the actual deployment of Alloy and the Demo services is a copy/paste of 2 simple commands. Having done the setups steps once, you can easily re-run the project with those 2 commands any time in the future, without having to remember all the steps you took on prior runs.

This project's resources can be used in enablement sessions focussed on topics such as: 
- Deploying Alloy into Kubernetes
- Protecting Grafana Cloud authentication tokens with Kubernetes Secrets
- Configuring Alloy to support Application Observability
- Managing telemetry; putting cardinality protection into place
- Understanding more about Alloy's component-based configuration system
- etc.

The OTel Demo itself is a good codebase for learning more about OTel instrumentation. If you have questions about the project and its services and instrumentation, we encourage you to reach out to the [OTel Demo Community on Slack](https://opentelemetry.io/community/end-user/slack-channel/) - there are many people sharing questions and ideas there. Also, all of the source code for the services is available and includes documentation; this project can be used as a way to further expand your knowledge of how OTel instrumentation works.

### Flux, Helm, and Kustomize

This is a Flux-based project: it uses Flux to deploy both Alloy and the OTel demo via their public Helm charts. There is also some use of Kustomize in this project.

Therefore, a secondary goal of this project is to help some users - for example, who might be starting off learning imperative-driven deployment techniques with tools like Helm - to start becoming familiar with some declarative, GitOps-driven practices, using tools like Flux.

Here are a few short YouTube videos you might want to check out for the basics of Flux+Helm; there are plenty of other options on the web as well.
- [Flux GitOps Tutorial - DevOps and GitOps for Kubernetes](https://www.youtube.com/watch?v=PFLimPh5-wo)
- [Kubernetes Deployments with Flux v2: Helm Basics](https://www.youtube.com/watch?v=UhV8kYcb9Mc)


<br>

## Repository Structure
This repo is based on [the monorepo example here](https://github.com/fluxcd/flux2-kustomize-helm-example).

As you learn more with Flux, you will likely start to come up with other ways to structure your own repositories; this project's goal with Flux is just to introduce the solution, vs. taking users into more advanced areas of repo setups.

If you have questions or just want to learn more about the monorepo concept, take a look at the page linked above, as well as the [Flux website](https://fluxcd.io/flux/guides/repository-structure/#monorepo).

<br>



