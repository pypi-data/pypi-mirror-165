class OPCODES:
    HEARTBEAT = 1  # [CLIENT] Indicates a hertbeat payload
    IDENTIFY = 2  # [CLIENT] Indicates an identify payload
    PRESENCE_UPDATE = 3  # [CLIENT] Indicates a presence update payload
    VOICE_STATE_UPDATE = 4  # [CLIENT] Indicates a voice state update payload
    RESUME = 6  # [CLIENT] Indicates a resume payload
    RECONNECT = 7  # [SERVER] Requests the client to resume the session
    INVALID_SESSION = 9  # [SERVER] Indicates an invalid WebSocket session
    HEARTBEAT_ACK = 11  # [SERVER] Indicates the server receives the client's heartbeat
    HELLO = 10  # [SERVER] Indicates the hello payload


class EVENTS:
    MESSAGE_CREATE = "MESSAGE_CREATE"  # Message was created
    READY = "READY"  # WebSocket session is ready
    SETTINGS_UPDATE = "USER_SETTINGS_UPDATE"  # User's settings were changed
