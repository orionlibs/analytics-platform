 #!/bin/bash

: '
This script requires that you have the following values exported:
export ALLOY_CLOUD_OTLP_URL=
export ALLOY_OTLP_USERNAME_BASE64=
export ALLOY_OTLP_PASSSWORD_BASE64=
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
  name: k8s-int-otlp-destinations
  namespace: collector
data:
  destinations-list: |-
    destinations:
    - name: otlp-gateway
      type: otlp
      url: $ALLOY_CLOUD_OTLP_URL
      protocol: http
      auth:
        type: basic
        usernameKey: username
        passwordKey: password
      secret:
        create: false
        name: grafanacloud-otlphttp-secret
        namespace: collector
      metrics: {enabled: true}
      logs: {enabled: true}
      traces: {enabled: true}
---
apiVersion: v1
kind: Secret
metadata:
  name: grafanacloud-otlphttp-secret
  namespace: collector
type: Opaque
data:
  username: $ALLOY_CLOUD_OTLP_USERNAME_BASE64
  password: $ALLOY_CLOUD_OTLP_PASSSWORD_BASE64
" | kubectl apply -f -
