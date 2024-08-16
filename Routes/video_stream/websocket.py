from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from Databases.redis_connection import redis_call_client
from Loggers.log import call_log
import json
import random
from Functions.function import get_sl_DateTime

router = APIRouter()

# Store connected users
connected_users = set()

# Store websocket connection
connections = {}

# Ongoing conferences
conferences = {}

# Start times of conferences
conference_start_times = {}


# Send user message
async def send_to_user(user_id: str, message: dict):
    try:
        user_ws = connections.get(user_id)
        if user_ws:
            await user_ws.send_text(json.dumps(message))
            call_log.info(f"Message sent to {user_id}: {message}")
        else:
            call_log.warning(f"Attempted to send message to non-existent connection for user {user_id}")
    except Exception as e:
        call_log.error(f"Error sending message to {user_id}: {e}")


# Handle the conference
async def handle_conference(websocket: WebSocket, user_id: str):
    if len(connected_users) >= 2:
        # Random select another user and create conference
        potential_users = [user for user in connected_users if user not in conferences and user != user_id]
        if potential_users:
            other_user = random.choice(potential_users)
            conferences[user_id] = other_user
            conferences[other_user] = user_id

            # Record the start time of the conference
            start_time = get_sl_DateTime()
            conference_start_times[(user_id, other_user)] = start_time

            # Send notification to users about the conference
            try:
                await websocket.send_text(json.dumps(
                    {"type": "conference_started", "peer_id": redis_call_client.get(other_user).decode("utf-8")}))
                await send_to_user(other_user, {"type": "conference_started",
                                                "peer_id": redis_call_client.get(user_id).decode("utf-8")})
                call_log.info(f"Conference started between {user_id} - {other_user}")
            except Exception as e:
                call_log.error(f"Error starting conference between {user_id} - {other_user} : {e}")
    else:
        await websocket.send_text(json.dumps({"type": "wait_for_users"}))
        call_log.info(f"User {user_id} is waiting for more users to join")


# Handle disconnection
async def handle_disconnection(disconnected_user: str):
    if disconnected_user in conferences:
        other_user = conferences.pop(disconnected_user)
        if other_user in conferences:
            del conferences[other_user]

        # Calculate the meeting duration
        start_time = conference_start_times.pop((disconnected_user, other_user), None) or \
                     conference_start_times.pop((other_user, disconnected_user), None)

        if start_time:
            end_time = get_sl_DateTime()
            meeting_duration = end_time - start_time
            call_log.info(
                f"Conference between {disconnected_user} and {other_user} ended. Duration: {meeting_duration}")

        potential_users = [user for user in connected_users if user not in conferences and user != other_user]

        # Check if there is another user to replace the disconnected one
        if potential_users:
            new_user = random.choice(potential_users)
            conferences[other_user] = new_user
            conferences[new_user] = other_user

            await send_to_user(other_user, {"type": "conference_user_replaced",
                                            "peer_id": redis_call_client.get(new_user).decode("utf-8")})
            await send_to_user(new_user, {"type": "conference_started",
                                          "peer_id": redis_call_client.get(other_user).decode("utf-8")})
            call_log.info(
                f"User {disconnected_user} disconnected. Replaced with {new_user} in conference with {other_user}.")
        else:
            await send_to_user(other_user, {"type": "waiting_for_users"})
            call_log.info(f"User {disconnected_user} disconnected. {other_user} is now waiting for new users.")
    else:
        call_log.info(f"User {disconnected_user} disconnected but was not in a conference.")


@router.websocket("/createConference/{user_id}/{peer_connection_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, peer_connection_id: str):
    await websocket.accept()
    connected_users.add(user_id)
    connections[user_id] = websocket  # Store the WebSocket connection
    redis_call_client.set(user_id, peer_connection_id)
    call_log.info(f"User {user_id} connected - peer connection id: {peer_connection_id}")

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "join_conference":
                await handle_conference(websocket, user_id)
    except WebSocketDisconnect:
        call_log.info(f"User {user_id} disconnected")
        try:
            connected_users.remove(user_id)
            del connections[user_id]  # Remove the WebSocket connection
            await handle_disconnection(user_id)
        except Exception as e:
            call_log.error(f"{e}")
    except Exception as e:
        call_log.error(f"Error in websocket endpoint: {e}")

