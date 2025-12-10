import { Trend } from 'k6/metrics';
import { sleep } from 'k6';

export let options = {
  thresholds: {
    checks: ["rate==1"],
  },
  scenarios: {
    contacts: {
      executor: "constant-vus",
      vus: 1,
      duration: "1s",
    },
  },
};

const testTrend = new Trend("test_trend")

export default function () {
  testTrend.add(1)
  testTrend.add(1)
  testTrend.add(2)
  testTrend.add(2)

  sleep(.1);
}

