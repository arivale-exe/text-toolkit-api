// Text Toolkit Bookmarklet
// Drag this to your bookmarks bar, or save as a bookmark with this as the URL.
// Select text on any page, click it, and get an instant extractive summary.
// Requires the Text Toolkit API running locally on port 8090.
//
// To install: create a bookmark whose Location is:
// javascript:(function(){var s=encodeURIComponent(getSelection().toString()||document.selection.createRange().text);var x=new XMLHttpRequest();x.open('POST','http://localhost:8090/v1/summarize',true);x.setRequestHeader('Content-Type','application/json');x.onload=function(){var r=JSON.parse(x.responseText);alert(r.summary.join('\n\n'))};x.onerror=function(){alert('Text Toolkit API not running on localhost:8090')};x.send(JSON.stringify({text:s,sentences:3}))})();
//
// (The same code, formatted for readability below.)
(function () {
  var text = getSelection()
    ? getSelection().toString()
    : document.selection.createRange().text;
  if (!text.trim()) {
    alert("Select some text first, then click the bookmarklet.");
    return;
  }
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:8090/v1/summarize", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 402) {
      alert("Payment required: Text Toolkit costs 0.10 USDC per call.");
    } else if (xhr.status === 200) {
      var r = JSON.parse(xhr.responseText);
      alert(r.summary.join("\n\n"));
    } else {
      alert("Error: " + xhr.statusText);
    }
  };
  xhr.onerror = function () {
    alert("Text Toolkit API is not running on localhost:8090. Run: python3 server.py");
  };
  xhr.send(JSON.stringify({ text: text, sentences: 3 }));
})();
