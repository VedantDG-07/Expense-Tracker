function register(){
    let u = document.getElementById("ruser").value;
    let p = document.getElementById("rpass").value;
    let cp = document.getElementById("rcpass").value;
    let msg = document.getElementById("msg");

    if(u === "" || p === "" || cp === ""){
        msg.innerHTML = "All fields are required ❌";
        msg.style.color = "red";
        return;
    }

    if(p !== cp){
        msg.innerHTML = "Passwords do not match ❌";
        msg.style.color = "red";
        return;
    }

    // // save data in localStorage
    // localStorage.setItem("username", u);
    // localStorage.setItem("password", p);

    msg.innerHTML = "Registration Successful ✅";
    msg.style.color = "green";
}
