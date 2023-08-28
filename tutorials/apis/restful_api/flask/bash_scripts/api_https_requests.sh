#!/bin/bash

# brew install jq

# Credentials 
API_URL="https://127.0.0.1:5000/tasks"
API_KEY="your_api_key"
CREDENTIALS="./credentials/cert.pem"
JWT_TOKEN="your-jwt-token"

# Send a POST request to create a task

curl -X POST \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"title": "Buy ice cream"}' \
  --cacert $CREDENTIALS \
  -k $API_URL;

curl -X POST \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"title": "Buy vegetables"}' \
  --cacert $CREDENTIALS \
  -k $API_URL;

  curl -X POST \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"title": "Buy coffee"}' \
  --cacert $CREDENTIALS \
  -k $API_URL;

curl -X POST \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"title": "Buy chips"}' \
  --cacert $CREDENTIALS \
  -k $API_URL;

# Send a PUT request to update a task

curl -X PUT \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"title": "Buy fruit", "done": true}' \
  --cacert $CREDENTIALS \
  -k $API_URL/1;

# Send a PATCH request to partially update a task

curl -X PATCH \
  -H "Content-Type: application/json" \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"done": true}' \
  --cacert $CREDENTIALS \
  -k $API_URL/2;

# Send a DELETE request to delete a task 

curl -X DELETE \
  -H "API-Key: $API_KEY" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  --cacert $CREDENTIALS \
  -k $API_URL/1


# Loop through tasks and delete if 'done' is true
tasks=$(curl -X GET -H "Content-Type: application/json" -H "API-Key: $API_KEY" -H "Authorization: Bearer $JWT_TOKEN" --cacert $CREDENTIALS -k $API_URL)

for task_id in $(echo "$tasks" | jq -r '.tasks[] | select(.done == true) | .id'); do
    echo "Deleting task $task_id..."
    curl -X DELETE -H "API-Key: $API_KEY" -H "Authorization: Bearer $JWT_TOKEN" --cacert $CREDENTIALS -k $API_URL/$task_id
done

echo "Done deleting tasks."

#Print tasks datasest after deletion of completed tasks
tasks=$(curl -X GET -H "Content-Type: application/json" -H "API-Key: $API_KEY" -H "Authorization: Bearer $JWT_TOKEN" --cacert $CREDENTIALS -k $API_URL)
pretty_json=$(echo -e "$tasks" | jq '.')
echo -e "\nRemaining tasks:"
printf "%b\n" "$pretty_json"