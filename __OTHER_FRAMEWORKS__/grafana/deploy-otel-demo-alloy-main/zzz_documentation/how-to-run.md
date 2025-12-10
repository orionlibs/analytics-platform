# Detail on running this project

## prerequisite tools to have ready

- an available and ready k8s cluster (k3d and GKE are the 2 I have tested against; with k3d, I typically run a cluster with 3 worker nodes and one master; YMMV)
- kubectl, configured and ready to talk to your k8s cluster
- k8s viewer tool of your choice (k9s, Lens, etc. - or even just using kubectl if you prefer)
- [flux CLI](https://fluxcd.io/flux/installation/#install-the-flux-cli) installed
- github
- IDE of your choice


<br>

## running the project
In this project, it is good to think of yourself as wearing 2 hats
- a Platform Engineer
- a Developer

The next steps are set up with that model in mind.

<br>

## 1) As a Platform Engineer: spin up the cluster
Do what you need to do to spin up a k8s cluster. I have run this project successfully both using k3d on a Mac laptop, and on GKE where I have the option to run a larger cluster. In any case, make sure you can:
- test kubectl is connected
- test that you can view the cluster with the viewer tool of your choice


<br>

## 2) As a Platform Engineer: pre-provision the cluster


### First fork, and then clone this repo.

Note the above: it explicitly says to fork before cloning. As you dig into Flux, you'll see why you need your own fork.

Once you've created your fork, then clone it to your machine. Be sure not to change the clone's directory name; the reason why will be more clear in a bit.

CD into the directory "deploy-otel-demo-alloy".

<br>


### Get your credentials for shipping to Grafana Cloud's OTLP endpoint

If you have not done this before, you might need some help from someone with access to a Grafana Cloud cluster (or go spin up a free account of your own). 

You will need to go to your Grafana Cloud portal (https://grafana.com/orgs/YOUR_ORG_NAME), then into the stack you wish to use, and then to the "OpenTelemetry" area on the "Manage your stack" page, and click the blue "Configure" button. There, you can get an OTLP write token, your user ID and the cloud endpoint for shipping OTLP over HTTP.

You will need to Base64-encode your OTLP write token, as it will be written into a K8s secret. Here's how to do that at the command prompt:
```
echo -n YOUR_TOKEN_HERE | base64
```
(The "-n" is important not to forget; if you don't include that, ```echo``` will include a newline, which will change the content of your token.)

Set these up as exports, replacing the "YOUR_" sections with your values:

```
export ALLOY_CLOUD_OTLP_URL=YOUR_URL_HERE
export ALLOY_CLOUD_OTLP_USERNAME=YOUR_USERNAME_HERE
export ALLOY_CLOUD_OTLP_PASSSWORD_BASE64=YOUR_BASE_64_ENCODED_TOKEN_HERE
```

Make sure that the file "./pre-provision/alloy.sh" is executable on your system.

<br>

### Run pre-provisioning

Now, as the Platform Engineer, you can pre-provision the ConfigMap and Secret needed by Alloy, so that it can ship telemetry to your Grafana Cloud instance. These resources will be deployed into a new namespace called "collector". Run the following:

```
./pre-provision/alloy.sh
```

You can use k9s or another viewing tool to check that the Namespace, ConfigMap and Secret have been created. 

<br>

## Change hats
At this point we shift over to wearing the Developer hat.

<br>

## 3) As a Dev team member: use GitOps practices (e.g. Flux) to deploy your microservices

Essentially we are following the same steps as here:
https://github.com/fluxcd/flux2-kustomize-helm-example/tree/main?tab=readme-ov-file#bootstrap-staging-and-production

Reading that page is highly recommended; however here's the quick set of steps to follow.

<br>

### check that the cluster is flux-compatible:
   flux check --pre

<br>

### create your PAT on GitHub
In GitHub, create a PAT (personal access token). If you want to use fine-grained tokens you are welcome to; this project only describes how to use Classic tokens. (For more details, please refer to the Flux documentation.)
- Go to [the "classic" tokens page on GitHub](https://github.com/settings/tokens)
- Create a new Personal Access Token (classic)
- enable it with Repo management rights (I've been clicking on the "Repo" checkbox and including all the sub-checkboxes; I'd welcome further testing of reducing these and seeing when things stop working).
- Scroll down to Generate Token and click it.
- In the next page, be sure to copy the token and put it somewhere safe on your machine (see exports next); it's the only time it will be shown.


<br>

### Set up environment variables
On your machine create these env vars, with appropriate values:

```
export GITHUB_TOKEN=[YOUR_PAT]
export GITHUB_USER=[YOUR_USERNAME]
```

> Minor note for the security-conscious: the GITHUB_TOKEN doesn't get stored in the cluster.
> Instead, the flux CLI uses the GITHUB_TOKEN locally to add a Deploy Key in the selected GitHub repo on bootstrap, so that flux (inside the cluster) is able to clone solely that repo.


<br>

### And finally: run flux bootstrap

You might want to take your time and just review the commands below before running them. The basic steps are:

- set up $BASENAME to be the name of the current directory (not the full path, just the directory name; it should still be the same as the repo name)
- run flux bootstrap
- ensure that the context is set to kubectl's current context
- get owner from your env vars
- Flux automatically looks for your PAT in your envionment (you exported the PAT earlier as "GITHUB_TOKEN").

```
CURRENT=`pwd`; BASENAME=`basename "$CURRENT"`; \
flux bootstrap github \
    --context=$(kubectl config current-context) \
    --owner=${GITHUB_USER} \
    --repository=${BASENAME} \
    --branch=main \
    --path=clusters/staging
```

<br>

### Watch things spin up
When running the bootstrap command, it can be helpful to do the following:

1) Using k9s, watch pods in all namespaces. You should see 4 Flux pods come up, followed shortly by 1 Alloy pod, and all of the OTel Demo's services (and not the demo's o11y stack pods).

2) In a separate terminal, run this command
```watch flux get all -A```

On a laptop, it can be helpful to reduce font size in that second terminal, to make the items stand out more clearly. If you dive deeper into Flux, and try out some new modifications of your own, the data returned by this command can be helpful in quickly identifying Flux resources that have not been set up correctly; they will stand out quite clearly in the output.

<br>


## View your telemetry in Grafana Cloud

Shortly after the system is fully booted, you should be able to see Traces, Logs and Metrics arriving in your cloud account. There will be metrics from the services themselves (search metric names for "ads" for example), and from the Metric Generator if you have that enabled in Cloud Traces.

A great way to see that telemetry is arriving is to go into Explore Logs - as of this writing, the default grouping is by Service Name, which makes it easy to see the set of demo services that export logs via OTLP ([not all of them do as of now](https://opentelemetry.io/docs/demo/telemetry-features/log-coverage/)).

In addition, if you have the Metric Generator enabled, you should be able to view the demo services in App O11y.

For logs to show correctly in App O11y, you may need to update your settings here [https://YOUR_STACK_NAME.grafana.net/a/grafana-app-observability-app/configuration/logs](https://YOUR_STACK_NAME.grafana.net/a/grafana-app-observability-app/configuration/logs), and set "Default log query format" to "OTLP Gateway / native Loki otlp query".



<br>

## Teardown:
This set of commands will uninstall Flux from the cluster, and then delete the namespaces created by this project.

```flux uninstall -s ; kubectl delete namespace collector ; kubectl delete namespaces open-telemetry```


