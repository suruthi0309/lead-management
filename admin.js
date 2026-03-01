
// load leads

function loadLeads(){

fetch("/api/leads")

.then(res=>res.json())

.then(data=>{

let body=document.getElementById("tableBody");

body.innerHTML="";

data.forEach(l=>{

body.innerHTML+=`

<tr>

<td>${l.name}</td>

<td>${l.mobile}</td>

<td>${l.email}</td>

<td>${l.service}</td>

<td>

<select
onchange="updateStatus(${l.id},this.value)">

<option ${l.status=="New"?"selected":""}>New</option>

<option ${l.status=="Prospect"?"selected":""}>Prospect</option>

<option ${l.status=="Hot"?"selected":""}>Hot</option>

<option ${l.status=="Closed"?"selected":""}>Closed</option>

</select>

</td>

<td>${l.created_at}</td>

</tr>

`;

});

});

}



// update status

function updateStatus(id,status){

fetch(`/api/leads/${id}`,{

method:"PUT",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

status:status

})

})

.then(()=>{

Swal.fire({

icon:"success",

title:"Updated",

text:"Lead Status Updated",

timer:1200,

showConfirmButton:false

});

});

}



// search

function searchLead(){

let input=

document.getElementById("search")
.value.toLowerCase();

let rows=

document.querySelectorAll("tbody tr");

rows.forEach(row=>{

row.style.display=

row.innerText.toLowerCase()
.includes(input)

? ""

:"none";

});

}