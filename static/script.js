function check(){
    let u = document.getElementById("user").value;
    let p = document.getElementById("pass").value;

    let su = localStorage.getItem("username");
    let sp = localStorage.getItem("password");

    let msg = document.getElementById("msg");

    if(u === su && p === sp){
    window.location.href = "dashboard.html";
    }
    else {
        msg.innerHTML = "Wrong Username or Password ❌";
        msg.style.color = "red";
    }
}
