#!/bin/bash

# brew install jq

API_URL="http://127.0.0.1:5000/tasks"

# Send a POST request to create a task

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy ice cream"}' \
  $API_URL;

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy vegetables"}' \
  $API_URL;

  curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy coffee"}' \
  $API_URL;

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy chips"}' \
  $API_URL;

# Send a PUT request to update a task

curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy fruit", "done": true}' \
  $API_URL/1;

# Send a PATCH request to partially update a task

curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"done": true}' \
  $API_URL/2;

# Send a DELETE request to delete a task 

curl -X DELETE $API_URL/1


# Loop through tasks and delete if 'done' is true
tasks=$(curl -X GET -H "Content-Type: application/json" $API_URL)

for task_id in $(echo "$tasks" | jq -r '.tasks[] | select(.done == true) | .id'); do
    echo "Deleting task $task_id..."
    curl -X DELETE $API_URL/$task_id
done

echo "Done deleting tasks."

#Print tasks datasest after deletion of completed tasks
tasks=$(curl -X GET -H "Content-Type: application/json" $API_URL)
pretty_json=$(echo -e "$tasks" | jq '.')
echo -e "\nRemaining tasks:"
printf "%b\n" "$pretty_json"