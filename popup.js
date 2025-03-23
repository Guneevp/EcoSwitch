document.getElementById("getUrlButton").addEventListener("click", async () => {
    // Get the current website URL
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
  
    // Send the URL to the backend
    try {
      const response = await fetch("http://127.0.0.1:5000/get-product-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });
  
      const data = await response.json();
      document.getElementById("result").innerText = `Product Name: ${data.productName}`;
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("result").innerText = "Failed to fetch product info.";
    }
  });