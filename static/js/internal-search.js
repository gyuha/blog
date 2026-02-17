(function () {
  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalize(value) {
    return (value || "").toString().toLowerCase().trim();
  }

  function snippet(value, keyword) {
    var text = (value || "").replace(/\s+/g, " ").trim();
    if (!text) return "";
    if (!keyword) return text.slice(0, 180);

    var lower = text.toLowerCase();
    var idx = lower.indexOf(keyword.toLowerCase());
    if (idx < 0) return text.slice(0, 180);

    var start = Math.max(0, idx - 60);
    var end = Math.min(text.length, idx + keyword.length + 120);
    var prefix = start > 0 ? "..." : "";
    var suffix = end < text.length ? "..." : "";
    return prefix + text.slice(start, end) + suffix;
  }

  async function loadIndex(url) {
    var response = await fetch(url, {headers: {Accept: "application/json"}});
    if (!response.ok) {
      throw new Error("Search index request failed: " + response.status);
    }
    return response.json();
  }

  function renderResults(results, keyword) {
    var metaNode = document.getElementById("search-meta");
    var resultsNode = document.getElementById("search-results");

    if (!keyword) {
      metaNode.textContent = "검색어를 입력해 주세요.";
      resultsNode.innerHTML = "";
      return;
    }

    metaNode.textContent = '"' + keyword + '" 검색 결과: ' + results.length + "건";

    if (!results.length) {
      resultsNode.innerHTML = '<div class="post-summary">검색 결과가 없습니다.</div>';
      return;
    }

    resultsNode.innerHTML = results
      .map(function (item) {
        var title = escapeHtml(item.title || "(제목 없음)");
        var link = escapeHtml(item.permalink || "#");
        var date = escapeHtml(item.date || "");
        var preview = escapeHtml(snippet(item.content || item.summary || "", keyword));
        return (
          '<article class="post">' +
          '<div class="post-title"><a href="' +
          link +
          '"><h3>' +
          title +
          "</h3></a></div>" +
          '<div class="post-summary">' +
          (date ? '<div class="post-meta"><time>' + date + "</time></div>" : "") +
          (preview ? "<p>" + preview + "</p>" : "") +
          "</div>" +
          "</article>"
        );
      })
      .join("");
  }

  async function init() {
    var params = new URLSearchParams(window.location.search);
    var keyword = params.get("q") || "";
    var input = document.getElementById("internal-search-input");
    var indexUrl = window.__SEARCH_INDEX_URL__ || "/index.json";

    if (input) {
      input.value = keyword;
    }

    try {
      var indexData = await loadIndex(indexUrl);
      var query = normalize(keyword);
      var filtered = indexData.filter(function (item) {
        var title = normalize(item.title);
        var summary = normalize(item.summary);
        var content = normalize(item.content);
        return title.includes(query) || summary.includes(query) || content.includes(query);
      });
      renderResults(filtered, keyword);
    } catch (error) {
      var metaNode = document.getElementById("search-meta");
      var resultsNode = document.getElementById("search-results");
      if (metaNode) {
        metaNode.textContent = "검색 데이터를 불러오지 못했습니다.";
      }
      if (resultsNode) {
        resultsNode.innerHTML = '<div class="post-summary">잠시 후 다시 시도해 주세요.</div>';
      }
      console.error(error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
