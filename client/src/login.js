userNameInput = document.getElementById("userNameInput");
passwordInput = document.getElementById("password");
loginBtn = document.querySelector(".btn");
alertMsg = document.querySelector(".alert");

//any state variables stored in state
state = {};

//function to login
const login = async function (userName, password){
    try{
        // 1) fetch data
        response = await fetch(`http://localhost:1313/users/login?user_name=${userName}&password=${password}`);
        response = await response.json();
        
        // 2) check status code of response
        if(response.status === 200){
            // a. remove any errors in state
            delete this.state.error;
            // b. successfully logged in
            this.state.user = response.data[0];
        }else{
            // b. an error occured
            this.state.error = response;
            throw Error();
        }
    }catch(e){
        // 1) propogate error up
        throw Error();
    }
}

//function to redirect
const redirectFromLogin = function(){
    // 1) check if user is employee or manager
    // and redirect accordingly
    if(state.user.role === "employee"){
        location.href = "employee-dash.html";
    }else if(state.user.role === "manager"){
        location.href = "manager-dash.html";
    }
}

//check if logged in and redirect
const checkIfLoggedIn = function(){
    // 1) retrieve data from local storage
    state = JSON.parse(localStorage.getItem('data'));
    // a. if user is logged in already, redirect
    if(state && state.user){
        setTimeout(redirectFromLogin, 200);
    
    // b. otherwise, reset state to empty 
    } else
        state = {}
}

//persist state variables into local storage
const persist = function(){
    // 1) store in local storage
    localStorage.setItem('data', JSON.stringify(state));
}


//add event listener to click button on login form
loginBtn.addEventListener("click", async e => {
    try{
        e.preventDefault();
        // 1) try to log in
        await login(userNameInput.value, passwordInput.value);
        // 2) persist data to localstorage
        persist();
        // 3) redirect to proper dashboard
        redirectFromLogin();
    
    // if error, show alert message
    }catch(e){
        alertMsg.classList.remove("hidden");
        alertMsg.innerHTML = state.error.message;
    }
});

//on page load, check if a user is already logged in
checkIfLoggedIn();