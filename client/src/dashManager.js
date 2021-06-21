const logoutBtn = document.getElementById('logout-btn');
const welcome = document.getElementById('welcome');
const contentDisplay = document.querySelector('.content');
const menuItems = document.querySelectorAll('.list-group-item');
const submitForm = document.getElementById('submit-my-form');
const formMessage = document.getElementById('form-message');
const radioApprove = document.getElementById('radio-approve');
const radioDeny = document.getElementById('radio-deny');
const invalidInputWarn = document.querySelector('.invalid-input-warn');

//any state variables stored in state
state = {};

//fetch ALL reimbursement data
const getAllReimbursements= async function(){
    //get reimbursements
    try{
        response = await fetch(`http://localhost:1313/reimbursements`);
        let body = await response.json();
        // 2) check status code of response
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. save body to local cache, sort by newest first
            state.allReimbursements = body.data[0];
            state.allReimbursements.sort((a,b) => b.createdAt - a.createdAt);
        }
    }catch(e){
        throw Error(e);
    }
}

const getAllEmployees = async function(){
    //get reimbursements
    try{
        response = await fetch(`http://localhost:1313/employees`);
        let body = await response.json();
        // 2) check status code of response
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. save body to local cache
            state.allEmployees = {}
            body.data[0].forEach(el => state.allEmployees[el.workerId] = `${el.firstName} ${el.lastName}`);
        }
    }catch(e){
        throw Error(e);
    }
}

const updateReimbursement = async function (managerId, reimbursementId, status, managerMessage){
    try{
        //delete cur updating from memory, not needed anymore
        delete state.curUpdadingId;
        
        let update = {
            "state":status,
            "managerMessage":managerMessage
        };

        response = await fetch(
            `http://localhost:1313/managers/${managerId}/reimbursements/${reimbursementId}`,
             {
                 method: 'PATCH',
                 headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                 },
                 body: JSON.stringify(update)
             });
        let body = await response.json();
        // 2) check status code of response
        if(response.ok){
            // a. remove any errors in state
            delete state.error;
            // b. update local cache of allReimbursements 
            state.allReimbursements = state.allReimbursements.filter(el => el.reimbursementId != body.data[0].reimbursementId); 
            state.allReimbursements.push(body.data[0]); 
        }else{
            state.error = response;
        }
    }catch(e){
        throw Error(e);
    }
}

//check if logged in and redirect
const checkIfLoggedInFromDash = function(){
    // 1) retrieve data from local storage
    state = JSON.parse(localStorage.getItem('data'));

    // a. if user is not logged in or user is not a manager, redirect
    redirectFromEmployeeDash();
}

//function to redirect
const redirectFromEmployeeDash = function(){
    // 1) check if user is logged in, employee or manager
    if(!state || !state.user){
        location.href = "login.html";
    }
    else if(state.user.role === "manager"){
        return;
    }else if(state.user.role === "employee"){
        location.href = "employee-dash.html";
    }
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

const renderAllReimbursementTable = function(){
    //return if reimbursements haven't finished loading
    if(!state.allReimbursements) return;
    
    rows = '';
    state.allReimbursements.forEach(el => {
        rows+= `
            <tr>
                <th scope="row" colspan="2">${state.allEmployees[el.employeeId]}</th>
                <td colspan="2">${el.reason} </td>
                <td></td>
                <td>${el.amount.toFixed(2)}</td>
                <td>${el.state}</td>
                <td>${el.state === 'pending' ?`<button class="btn btn-primary bg-info no-border btn-sm" id="update-btn" data-toggle="modal" data-target="#exampleModal" onclick="storeIdOfCurrentEdit(event)" data-id=${el.reimbursementId}>Decide</button>`:``}</td>
            </tr>`;
    });
   
    if( rows === ''){
        rows += `
        <tr>
            <th> No reimbursemetns to show</th>
            <td colspan="7"></td>
        </tr>`
    }

    contentDisplay.innerHTML = `
        <table class="table table-hover border table-fixed" id ='reimbursement-table'>
            <div class="alert alert-success reimbursement-alert hidden" role="alert" id="creation-alert">
                
            </div>
            <thead>
                <tr>
                    <th colspan="8">All Reimbursements</th>
                </tr>
                <tr>
                    <th scope="col" colspan="2">Name</th>
                    <th scope="col" colspan="2">Reason</th>
                    <th></th>
                    <th scope="col">Amount</th>
                    <th scope="col">Status <i class="fas fa-caret-down" id="sort-desc" onclick="sortTableByStatus(event)"></i><i class="fas fa-caret-up" id="sort-asc" onclick="sortTableByStatus(event)"></i></th>
                    <th scope="col">Deny/Accept</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>`;
}

const renderAnalytics = function(){
    /*-------------- CHART 1 ---------------*/
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart1);

    //month name list
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    //get the month for all reimbursement from their epoch
    const expensesByMonth = state.allReimbursements.map(cur => {
        let rMonth = monthNames[new Date(cur.createdAt).getMonth()];
        if(cur.state === 'approved'){
            return [rMonth, cur.amount];
        }else{
            return [rMonth, 0];
        }
    });
    
    //get the month totals
    const monthTotals = {};
    expensesByMonth.forEach(cur => {
        if(!monthTotals[cur[0]]) monthTotals[cur[0]] = 0;
        monthTotals[cur[0]] += cur[1];
    });
    
    //convert table data to array
    let tableData1 = [];
    for(const [key, value] of Object.entries(monthTotals)) {
        tableData1.unshift([key, value]);
    }

    function drawChart1() {
        let data = google.visualization.arrayToDataTable(
            [
                ['Month', 'Totals'],
                ...tableData1
            ]
        );

        let options = {
            title: '',
            hAxis: {title: 'Month',  titleTextStyle: {color: '#333'}},
            vAxis: {title: 'Amount', minValue: 0},
            height: 300,
            width: 750,
            series: {
                0: { color: '#1c91c0' },
                1: { color: '#e7711b' }
            }
        };

        let chart = new google.visualization.AreaChart(document.getElementById('chart_main'));
        chart.draw(data, options);
    }

    /*-------------- CHART 2 ---------------*/
    // Load google charts
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart2);

    //get all expenses with user name
    const expensesByUser = state.allReimbursements.map(cur => {
        if(cur.state === 'approved')
            return [state.allEmployees[cur.employeeId], cur.amount];
        else{
            return [state.allEmployees[cur.employeeId], 0];
        }
    });

    //get mapOfUserToExpenses
    const mapUserToExpense = {}
    expensesByUser.forEach(cur => {
        if(!mapUserToExpense[cur[0]]) mapUserToExpense[cur[0]] = 0;
        mapUserToExpense[cur[0]] += cur[1];
    });
    
    //generate data in array format
    let tableData2 = [];
    for(const [key, value] of Object.entries(mapUserToExpense)) {
        tableData2.unshift([key, value]);
    }


    // Draw the chart and set the chart values
    function drawChart2() {
        let data = google.visualization.arrayToDataTable([
        ['Employee', 'Reimbursements This Year'],
        ...tableData2
        ]);

        // Optional; add a title and set the width and height of the chart
        let options2 = {'title':'', height: 300, width: 500};

        // Display the chart inside the <div> element with id="piechart"
        let chart1 = new google.visualization.PieChart(document.getElementById('piechart'));
        chart1.draw(data, options2);
    }
    
    contentDisplay.innerHTML = `
    <i class="fa fa-refresh" aria-hidden="true" id="refresh-btn"></i>
    <div class="chart-outer-container">
        <div class="chart">
        <h4 class= "chart-title">Total Company Expenses 2021</h4>
        <div id="chart_main"></div>
        </div>
        <div class="chart">
            <h4 class= "chart-title">Employee Expense Percentage</h4>
            <div id="piechart"></div>
        </div>
    </div>`;
    //add thet event listener to refresh page
    const refreshBtn = document.getElementById('refresh-btn');
    //refresh event listener
    refreshBtn.addEventListener('click', renderAnalytics);
}

const renderOther = function(){
    contentDisplay.innerHTML = `<h1 class= "other">...sectiton coming soon.</h1>`;
}

const sortTableByStatus = function(e){
    // sort desc
    if(e.target.classList.contains("fa-caret-down")){
        state.allReimbursements.sort((a,b) => a.state.localeCompare(b.state));
        e.target.classList.add('hidden');
    // sort asc
    }else{
        state.allReimbursements.sort((a,b) => b.state.localeCompare(a.state));
        e.target.classList.add('hidden');
    }
    renderAllReimbursementTable();
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

//store ID of current update
const storeIdOfCurrentEdit = function(e){
    state.curUpdadingId = e.target.dataset.id;
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

//refreshBtn handler
const refreshAnalytics = async function(){
     //load all reimbursements
     await getAllReimbursements();
    
     //load get all users
     await getAllEmployees();
 
     //render account page
     renderAccountInfo();
}

//update welcome message
const updateWelcomeMessage = function(){
    welcome.innerHTML = `Welcome,  ${state.user.firstName}!`
}

//initialize manager-dash page
const onPageLoad = async function(){
    //check if logged in and get state
    checkIfLoggedInFromDash();

    //update welcome message
    updateWelcomeMessage();

    //load all reimbursements
    await getAllReimbursements();
    
    //load get all users
    await getAllEmployees();

    //render account page
    renderAccountInfo();
}

//update the dashboard
const updateDashboard = function(e){
    e.preventDefault();

    //return if data hasn't arrived yet
    if(!state.allReimbursements || !state.allEmployees) return;

    // 1) remove bolded out menu item
    removeSelectedFromMenuItems();

    // 2) highlight correct menu item
    e.target.classList.remove('text-white');
    e.target.classList.add('selected');

    // 3) update dash content
    if(e.target.id==='account'){
        renderAccountInfo();
    }else if(e.target.id === 'reimbursements'){
        renderAllReimbursementTable();
    }else if(e.target.id==='analytics'){
        renderAnalytics();      
    }else{
        renderOther();
    }    
}

/*Event Listeners*/
menuItems.forEach(cur => cur.addEventListener('click', updateDashboard));

//Add Event Listener for logout btn
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    logOut();
});

//Add Event Listener for submit-form use event delegation
submitForm.addEventListener('click', async e => {
    try{
        e.preventDefault();
        let newState = radioApprove.checked ? 'approved':'denied';
        //send update request and update in cache
        await updateReimbursement(state.user.workerId.toString(), state.curUpdadingId, newState, formMessage.value); 
        
        //update to UI
        renderAllReimbursementTable();
        //give alert message
        toggleTableAlert('Updated successfully!', 'alert-success');

        
    } catch(e){
        toggleTableAlert('Failed to update!', 'alert-danger'); 
    }
});

onPageLoad();