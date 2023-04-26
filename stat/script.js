const uuid = new URLSearchParams(window.location.search).get("uuid");
fetch("/stat/list.json")
  .then((res) => res.json())
  .then((json_res) => {
    li = "";

    for (let d = 0; d < json_res.domains.length; d++) {
      urlObj = json_res.domains[d];
      added = ""
      about = urlObj.about.split("#")


      if (about.includes("arvan")) {
        added += `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="fill: #00baba;padding: 1px;" viewBox="0 0 16 16">
        <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
      </svg>`
      }
      if (about.includes("cloudflare")) {
        added += `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="fill: #ee730a;padding: 1px;" viewBox="0 0 16 16">
        <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
      </svg>`
        added += `<small style="padding: 4px;">risky</small>`
      }
      if (about.includes("mtn")) {
        added += `<small style="padding: 4px;">mtn</small>`
      }
      if (about.includes("mci")) {
        added += `<small style="padding: 4px;">mci</small>`
      }

      if (about.includes("tci")) {
        added += `<small style="padding: 4px;">tci</small>`
      }


      console.log(about)
      base_vmess = `{"add": "${urlObj.d}", "ps": "${urlObj.d}", "scy": "auto", "type": "", "sni": "", "path": "/ws/","port": 443, "v": 2, "host": "", "tls": "tls", "id": "${uuid}", "net": "ws"}`;

      li += `<li  class="list-group-item d-flex justify-content-between align-items-center">
      <p><small>${urlObj.d}</small> | ${added}</p>
      
      <a href="https://ar3642.top/qr?str=vmess://${btoa(
        base_vmess
      )}">vmess</a>
        </li>`;
    }
    document.getElementById("content").innerHTML = `<ul>${li}</ul>`;
  });