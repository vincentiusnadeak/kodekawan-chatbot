const log = document.getElementById("log"), form = document.getElementById("form"), input = document.getElementById("input");
let history = [];

function esc(s){return s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function render(text){
  return esc(text)
    .replace(/```(\w*)\n([\s\S]*?)```/g,(_,l,c)=>`<pre><code>${c}</code></pre>`)
    .replace(/`([^`]+)`/g,"<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g,"<b>$1</b>")
    .replace(/\n/g,"<br>").replace(/<\/pre><br>/g,"</pre>").replace(/<br><pre>/g,"<pre>");
}
function add(role, text){
  const d = document.createElement("div");
  d.className = "msg " + role; d.innerHTML = render(text);
  log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
}
add("bot","Halo! Aku **KodeKawan**, tutor pemrogramanmu. Pilih gaya bahasa dan domain di samping, lalu tanya apa saja ya!");

async function send(text){
  add("user", text); history.push({role:"user",content:text});
  const wait = add("bot","Sedang mengetik...");
  const res = await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({messages:history,style:style.value,domain:domain.value,memory:memory.checked})});
  const data = await res.json();
  wait.innerHTML = render(data.reply); history.push({role:"assistant",content:data.reply});
  log.scrollTop = log.scrollHeight;
}
form.addEventListener("submit",e=>{e.preventDefault();const t=input.value.trim();if(!t)return;input.value="";send(t);});
document.querySelectorAll(".hint a").forEach(a=>a.onclick=()=>send(a.dataset.q));
document.getElementById("reset").onclick=async()=>{await fetch("/api/reset",{method:"POST"});history=[];log.innerHTML="";add("bot","Memory dan riwayat chat sudah dihapus.");};
