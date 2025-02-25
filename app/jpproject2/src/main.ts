import { Html5QrcodeScanner } from "html5-qrcode";

// ...existing code...

const html5QrcodeScanner = new Html5QrcodeScanner(
    "reader",
    { fps: 10, qrbox: 250 },
    false
);

html5QrcodeScanner.render(
    (decodedText, result) => {
        // Handle on success condition with the decoded text or result.
        console.log(`Scan result: ${decodedText}`);
        
        // Display the decoded text in a text element
        const resultElement = document.getElementById("result");
        if (resultElement) {
            resultElement.innerText = `Decoded Text: ${decodedText}`;
        }
    },
    (errorMessage) => {
        // Handle on error condition with the error message.
        console.log(`Scan error: ${errorMessage}`);
    }
);

// ...existing code...

// Add a text element to display the decoded text
const resultContainer = document.createElement("div");
resultContainer.id = "result";
document.body.appendChild(resultContainer);
