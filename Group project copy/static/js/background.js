chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
      // Example: Block requests containing "ad" in the URL
      if (details.url.includes("ad")) {
        return { cancel: true };
      }
      return { cancel: false };
    },
    { urls: ["<all_urls>"] },
    ["blocking"]
  );
  