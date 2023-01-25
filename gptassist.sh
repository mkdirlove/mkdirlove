#!/bin/bash

# My fancy banner
clear
echo "DefacerPH x ChatGPT" | toilet -f smbraille
echo ""  

# Set the API key from the environment variable or directly in the script
# Replace "my key" with your actual API key
API_KEY="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"

# Set the endpoint URL for the OpenAI API
ENDPOINT_URL="https://api.openai.com/v1/completions"

# Start a new conversation by deleting the old one
rm -f ./chat.log

# Continuously ask for questions
while true; do

# Display a prompt for the user to enter their question
printf "\033[1m@You > \033[0m"

# Read the user's question
read -r QUESTION

# Write the question into the chat.log
echo -n "human: $QUESTION " >> ./chat.log

# Add some nice terminal formatting
tput sgr0
echo -e "\e[1m------------"

# Read the chat.log, including the user's last question, ready to send to chatGPT
QUERY=`cat ./chat.log`

# Set the JSON payload for the request
payload="{
    \"model\":\"text-davinci-003\",
    \"prompt\":\"$QUERY\",
    \"max_tokens\": 4000,
    \"temperature\": 1"

# Close the JSON payload
payload="$payload }"

# Send the request to the OpenAI API
response=$(curl -sS -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $API_KEY" -d "$payload" "$ENDPOINT_URL" 2>&1)

# Extract the response from the JSON object
RESPONSE_MESSAGE=$(echo "$response" | jq -r '.choices[0].text')

# Print the response
echo -e "\n"
printf "\033[1m@ChatGPT / OpenAI > \033[0m"
echo "$RESPONSE_MESSAGE"

# Write the response into a reponse.log
echo -n "ai:$RESPONSE_MESSAGE " > ./response.log

# Remove rogue new-line formatting and add the response to the chat.log
echo -n "$(<./response.log )" | tr -d '\n' >> ./chat.log

# More fancy terminal formatting
echo -e "\e[1m------------\n"

done
