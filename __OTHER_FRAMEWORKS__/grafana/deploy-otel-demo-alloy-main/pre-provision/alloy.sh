#!/bin/bash

: '
This script requires that you have the following values exported:
export ALLOY_CLOUD_OTLP_URL=
export ALLOY_CLOUD_OTLP_USERNAME=
export ALLOY_CLOUD_OTLP_PASSSWORD_BASE64=
'

echo "
---
apiVersion: v1
kind: Namespace
metadata:
  name: collector
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafanacloud-otlphttp-configmap
  namespace: collector
data:
  url: "\"$ALLOY_CLOUD_OTLP_URL\""
  username: "\"$ALLOY_CLOUD_OTLP_USERNAME\""
---
apiVersion: v1
kind: Secret
metadata:
  name: grafanacloud-otlphttp-secret
  namespace: collector
type: Opaque
data:
  password: $ALLOY_CLOUD_OTLP_PASSSWORD_BASE64
" | kubectl apply -f -
