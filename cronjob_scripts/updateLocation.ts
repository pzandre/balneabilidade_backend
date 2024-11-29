export default async function(interval: Interval) {
  await fetch(Deno.env.get("BACKEND_URL") + "management/locations/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Api-Key ${Deno.env.get("BACKEND_API_KEY")}`,
    },
  });
  await fetch(Deno.env.get("BACKEND_URL") + "locations/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Api-Key ${Deno.env.get("BACKEND_API_KEY")}`,
    },
  });
}