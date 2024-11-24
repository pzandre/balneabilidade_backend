export default async function(interval: Interval) {
  await fetch(Deno.env.get("BACKEND_URL") + "management/weather/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Api-Key ${Deno.env.get("BACKEND_API_KEY")}`,
    },
  });
}