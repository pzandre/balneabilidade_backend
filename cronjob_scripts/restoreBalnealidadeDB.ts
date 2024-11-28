export default async function(interval: Interval) {
  await fetch(
    Deno.env.get("BACKEND_URL") + "management/initiate_restore_process/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Api-Key ${Deno.env.get("BACKEND_API_KEY")}`,
      },
      body: JSON.stringify({
        key: "latest.pgdump",
        bucket_name: "cron_dump",
      }),
    },
  );
}