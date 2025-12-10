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
