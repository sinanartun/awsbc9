// Function to extract tweets from the page
async function extractTweets() {
  const tweets = [];
  // Select all div elements with data-testid="cellInnerDiv"
  const tweetElements = document.querySelectorAll('div[data-testid="cellInnerDiv"]');

  tweetElements.forEach((tweetElement) => {
    // Collect all inner text within the div
    const tweetText = Array.from(tweetElement.childNodes)
      .map(node => node.innerText || node.textContent)
      .join(' ')
      .trim();
    if (tweetText) {
      tweets.push({ element: tweetElement, text: tweetText });
    }
  });

  return tweets;
}

// Function to send POST request to API for sentiment analysis
async function sendTweetForAnalysis(tweetObj) {
  const url = 'https://twitter2.github.rocks/sentiment/';
  const data = {
    text: tweetObj.text
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    if (response.ok) {
      const result = await response.json();
      console.log(`Tweet: "${tweetObj.text}" - Sentiment Analysis Result:`, result);
      if (result.sentiment === 'bearish') {
        tweetObj.element.style.backgroundColor = 'darkred';
      } else if (result.sentiment === 'bullish') {
        tweetObj.element.style.backgroundColor = 'darkgreen';
      }
    } else {
      console.error(`Failed to send tweet: "${tweetObj.text}" - Status: ${response.status}`);
    }
  } catch (error) {
    console.error(`Error sending tweet: "${tweetObj.text}" - ${error}`);
  }
}

// Function to log tweets to the console and send them for analysis
async function processTweets(tweets) {
  for (const tweetObj of tweets) {
    console.log(tweetObj.text);
    await sendTweetForAnalysis(tweetObj);
  }
}

// Initial run to capture tweets on page load
(async () => {
  const tweets = await extractTweets();
  await processTweets(tweets);
})();

// Observe changes to the Twitter feed and extract new tweets
const observer = new MutationObserver(async () => {
  const newTweets = await extractTweets();
  await processTweets(newTweets);
});

observer.observe(document, { childList: true, subtree: true });
