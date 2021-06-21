const logoutBtn = document.getElementById('logout-btn');
const welcome = document.getElementById('welcome');
const contentDisplay = document.querySelector('.content');
const menuItems = document.querySelectorAll('.list-group-item');
const submitForm = document.getElementById('submit-my-form');
const formReason = document.getElementById('form-reason');
const formAmount = document.getElementById('form-amount');
const invalidInputWarn = document.querySelector('.invalid-input-warn');

/**These elements DO NOT EXIST on initial page load.*/
/*But need listeners and will be important in E2E Testing: */
/**
/* @param tableAlert get from class = 'alert-table'
/* @param deleteBtn  get from class = 'delete-btn'  
*/

//any state variables stored in state
state = {};

//fetch cur user's reimbursement data
const getReimbursements= async function(){
    //get reimbursements
    try{
        response = await fetch(`http://localhost:1313/employees/${state.user.workerId}/reimbursements`);
        let body = await response.json();
        // 2) check status code of response
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. save body to local cache and sort newest first
            state.reimbursements = body.data[0];
            state.reimbursements.sort((a,b) => b.createdAt - a.createdAt);
        }
    }catch(e){
        throw Error(e);
    }
}

const deleteReimbursement = async function(employeeId, reimbursementId){  
    try{
        response = await fetch(
            `http://localhost:1313/employees/${employeeId}/reimbursements/${reimbursementId}`,
             {
                 method: 'DELETE'
             });
        // 2) check status code of response
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. save body to local cache
            state.lastDeleted = state.reimbursements.find(r => r.reimbursementId === reimbursementId*1);
        }else{
            state.error = response;
        }
    }catch(e){
        throw Error(e);
    }
}


const createReimbursement = async function(amount, reason){
    try{
        let reimbursement = {
            reimbursementId: 0,
            createdAt: 0,
            amount: (amount*1).toFixed(2).toString(),
            reason: reason,
            state: "",
            file: null,
            employeeId: state.user.workerId,
            managerId: null,
            managerMessage: null
        }
        response = await fetch(
            `http://localhost:1313/reimbursements`,
             {
                 method: 'post',
                 headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                 },
                 body: JSON.stringify(reimbursement)
             });
        let body = await response.json();
        // 2) check that response success
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. save body to local cache
            state.lastCreated = body.data[0];
            state.reimbursements.push(state.lastCreated);
        }else{
            state.error = response;
        }
    }catch(e){
        throw Error(e);
    }
}

//function to redirect
const redirectFromEmployeeDash = function(){
    // 1) check if user is logged in, employee or manager
    if(!state || !state.user){
        location.href = "login.html";
    }
    else if(state.user.role === "employee"){
        return;
    }else if(state.user.role === "manager"){
        location.href = "manager-dash.html";
    }
}

// function to logout
const logOut = function(){
    // 1) clear state
    state = {};

    // 2) clear local storage 
    localStorage.clear();
    
    // 3) redirect to login page
    redirectFromEmployeeDash();
}

//check if logged in and redirect
const checkIfLoggedInFromDash = function(){
    // 1) retrieve data from local storage
    state = JSON.parse(localStorage.getItem('data'));

    // a. if user is not logged in or user is a manager, redirect
    if(!state || !state.user) redirectFromEmployeeDash();
}

//update welcome messaage in dashboard
const updateWelcomeMessage = function(){
    welcome.innerHTML = `Welcome,  ${state.user.firstName}!`
}

const clearContentSection = function(){
    contentDisplay.innerHTML = "";
}


//render Account information
const renderAccountInfo = function(){
    contentDisplay.innerHTML = `
        <div class="about-section">
            <h3>Lorem Ipsum</h3>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aliquid laboriosam adipisci rerum culpa distinctio dicta corrupti doloribus fugit dolorem repudiandae!</p>
            <h3>Lorem Ispum Dolor</h3>
            <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Officiis vel maiores molestias quae explicabo fugiat. Quo, reiciendis, tempora quas, illo sint obcaecati consectetur eaque dicta perferendis beatae nam nesciunt ut!</p>
            <h3>Lorem</h3>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quia aspernatur ea laudantium commodi nisi sequi!</p>
        </div>`;
}

const renderReimbursementTable = function(){
    rows = '';
    state.reimbursements.forEach(el => {
        bg = el.state === "approved" ? "bg-granted": el.state === "pending" ? "bg-pending":"bg-denied";
        rows+= `
            <tr class= '${bg}'>
                <th scope="row">${el.reimbursementId}</th>
                <td colspan="1">${el.reason} </td>
                <td>${el.amount.toFixed(2)}</td>
                <td>${el.state}</td>
                <td>${el.managerMessage ? el.managerMessage: ''}</td>
                <td>${el.state === 'pending' ?`<button class="btn btn-primary bg-danger no-border btn-sm" id="delete-btn" data-id=${el.reimbursementId}>Delete</button>`:``}</td>
            </tr>`;
    });

    if( rows === ''){
        rows += `
        <tr>
            <th> No reimbursemetns to show</th>
            <td colspan="1"></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>`
    }

    contentDisplay.innerHTML = `
        <table class="table table-hover border table-fixed" id ='my-reimbursement-table'>
            <div class="alert alert-success reimbursement-alert hidden" role="alert" id= "creation-alert">
                
            </div>
            <thead>
                <tr>
                    <th colspan="5">My Reimbursement Requests</th>
                    <th><button class="btn btn-success no-border btn-sm" data-toggle="modal" data-target="#exampleModal" id='create-new-btn'>+New</button></th>
                </tr>
                <tr>
                    <th scope="col">Id</th>
                    <th scope="col">Reason</th>
                    <th scope="col">Amount</th>
                    <th scope="col">Status <i class="fas fa-caret-down" id="sort-desc" onclick="sortTableByStatus(event)"></i><i class="fas fa-caret-up" id= "sort-asc" onclick="sortTableByStatus(event)"></i></th>
                    <th scope="col">Message</th>
                    <th scope="col">Delete</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>`;
}

const renderOther = function(){
    contentDisplay.innerHTML = `<h1 class= "other">...sectiton coming soon.</h1>`;
}

//function to remove bold text from menu items
const removeSelectedFromMenuItems = function(){
    menuItems.forEach(cur => {
        if(cur.classList.contains('selected')){
            cur.classList.remove('selected');
            cur.classList.add('text-white');
        }
    });
}

const sortTableByStatus = function(e){
    // sort desc
    if(e.target.classList.contains("fa-caret-down")){
        state.reimbursements.sort((a,b) => a.state.localeCompare(b.state));
        e.target.classList.add('hidden');
    // sort asc
    }else{
        state.reimbursements.sort((a,b) => b.state.localeCompare(a.state));
        e.target.classList.add('hidden');
    }
    renderReimbursementTable();
}

const updateDashboard = function(e){
    e.preventDefault();
    // return if data isn't laoded yet
    if(!state.reimbursements) return;

    // 1) remove bolded out menu item
    removeSelectedFromMenuItems();

    // 2) highlight correct menu item
    e.target.classList.remove('text-white');
    e.target.classList.add('selected');

    // 3) update dash content
    if(e.target.id == "account"){
        renderAccountInfo();
    }else if(e.target.id == "my-reimbursements"){
        renderReimbursementTable();
    }else{
        renderOther();      
    }   
}

// things to do when this page is visited
const onPageLoad = async function(){
    //1) first check if user is authorized to see this page
    checkIfLoggedInFromDash();

    //2) next, update welcome message
    updateWelcomeMessage();

    //3) load user reimbursement requests 
    await getReimbursements();

    //4) render account info
    renderAccountInfo();
}

//Add Event Listeners for menu items
menuItems.forEach(cur => cur.addEventListener('click', updateDashboard));

//Add Event Listener for logout btn
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    logOut();
});

//Event listener for creating reimbursement
submitForm.addEventListener('click', async e => {
    try{
        // 0) check if number field has a valid value
        if (!formAmount.value) {
            //prevent submit button from closing modal
            e.stopImmediatePropagation();
            
            //show warning then hide after 1 second then return
            invalidInputWarn.classList.remove('hidden');
            setTimeout(()=> invalidInputWarn.classList.add('hidden'), 1750);
            return;
        }
        // 1) send post request
        await createReimbursement(formAmount.value, formReason.value);
        
        // 2) clear form fields and remove warning if there
        formAmount.value = formReason.value = '';

        // 3) update to dom
        renderReimbursementTable();

        // 4) give a success alert
        toggleTableAlert('Created successfully!', 'alert-success');
    }catch(e){
        toggleTableAlert('Failed to create new reimbursement!', 'alert-danger');
    }
});

// toggle the alert for table actions
const toggleTableAlert = ( message, elemId) => {
    //give alert for successful, leave for 1.5s
    let tableAlert = document.querySelector('.reimbursement-alert');
    tableAlert.classList.remove('hidden', 'alert-primary');
    tableAlert.classList.add(elemId);
    tableAlert.innerHTML = message;

    //hide alert and reset all
    setTimeout(() => {
        tableAlert.classList.remove(elemId);
        tableAlert.classList.add('hidden');
        tableAlert.classList.add('alert-primary');
        tableAlert.innerHTML = '';
    }, 2100);
}

//Add Event Listener for delete btn use event delegation
window.addEventListener('click', async e => {
    try{
        e.preventDefault();
        if(e.target.id == 'delete-btn'){
            //send delete request
            await deleteReimbursement(`${state.user.workerId}`, e.target.dataset.id); 
            
            //update reimbursements in state
            state.reimbursements = state.reimbursements.filter(r => r.reimbursementId != e.target.dataset.id);
            
            //update to UI
            renderReimbursementTable();

            //give alert message
            toggleTableAlert('Deleted successfully!', 'alert-success');

        }
    } catch(e){
        toggleTableAlert('Failed to delete alert!', 'alert-danger');
    }
});

//on page refresh
onPageLoad();