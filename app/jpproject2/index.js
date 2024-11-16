const socket = new WebSocket("ws://10.220.8.180:8765");

socket.onopen = () => {
    console.log("Connected to the server");
    socket.send("070847022909");
};

socket.onmessage = (event) => {
    console.log("Search result:", event.data);
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};