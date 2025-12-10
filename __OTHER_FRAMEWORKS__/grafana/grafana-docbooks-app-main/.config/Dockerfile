ARG grafana_version=latest
ARG grafana_image=grafana-enterprise

FROM grafana/${grafana_image}:${grafana_version}

ARG livereload_domain=localhost:35729
ARG anon_org_role=Admin

# Make it as simple as possible to access the grafana instance for development purposes
# Do NOT enable these settings in a public facing / production grafana instance
ENV GF_AUTH_ANONYMOUS_ORG_ROLE ${anon_org_role}
ENV GF_AUTH_ANONYMOUS_ENABLED "true"
ENV GF_AUTH_BASIC_ENABLED "false"
# Set development mode so plugins can be loaded without the need to sign
ENV GF_DEFAULT_APP_MODE "development"

# Inject livereload script into grafana index.html
USER root
RUN if echo "${livereload_domain}" | grep -q -E 'localhost:[0-9]+'; then \
        sed -i "s|</body>|<script src=\"http://${livereload_domain}/livereload.js\"></script></body>|g" /usr/share/grafana/public/views/index.html; \
    else \
        sed -i "s|</body>|<script src=\"http://${livereload_domain}/livereload/livereload.js?port=80\"></script></body>|g" /usr/share/grafana/public/views/index.html; \
    fi

