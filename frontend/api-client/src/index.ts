import createClient from "openapi-fetch";

import type { paths } from "./schema";

export function createApiClient(baseUrl: string, accessToken?: () => string | null) {
  const client = createClient<paths>({ baseUrl });
  if (accessToken) {
    client.use({
      onRequest({ request }) {
        const token = accessToken();
        if (token) {
          request.headers.set("Authorization", `Bearer ${token}`);
        }
        return request;
      },
    });
  }
  return client;
}
