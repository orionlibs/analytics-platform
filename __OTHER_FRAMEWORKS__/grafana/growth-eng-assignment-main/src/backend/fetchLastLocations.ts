import { faker } from "@faker-js/faker";

interface MockApiResponse {
  address: {
    street: string;
    city: string;
    id: string;
  };
}

let citiesDb: string[] = [];

for (var i = 0; i < 5; i++) {
  citiesDb = [...citiesDb, faker.location.city()];
}

export function fetchLastLocation(): Promise<MockApiResponse> {
  return new Promise((resolve) => {
    const delay = 100 + Math.random() * 1200;

    const mockApiResponse = {
      address: {
        id: faker.string.uuid(),
        street: faker.location.streetAddress(),
        city: citiesDb[Math.floor(Math.random() * citiesDb.length)],
      },
    };

    setTimeout(() => {
      resolve(mockApiResponse);
    }, delay);
  });
}
