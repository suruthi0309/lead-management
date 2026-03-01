async function submitLead(){

let name = document.getElementById("name").value.trim();
let mobile = document.getElementById("mobile").value.trim();
let email = document.getElementById("email").value.trim();
let service = document.getElementById("service").value;
let message = document.getElementById("message").value;

// ----------------------------
// Frontend Validation
// ----------------------------

if(name === "" || mobile === ""){
Swal.fire({
icon:"error",
title:"Required",
text:"Name and Mobile Required"
});
return;
}

// Mobile must be 10 digits
if(!/^\d{10}$/.test(mobile)){
Swal.fire({
icon:"error",
title:"Invalid Mobile",
text:"Mobile number must be exactly 10 digits"
});
return;
}

// Email must end with @gmail.com (if entered)
if(email !== "" && !/^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(email)){
Swal.fire({
icon:"error",
title:"Invalid Email",
text:"Email must end with @gmail.com"
});
return;
}

// ----------------------------
// Show Loading
// ----------------------------

Swal.fire({
title:"Submitting...",
allowOutsideClick:false,
didOpen:()=>{
Swal.showLoading();
}
});

// ----------------------------
// Send Data
// ----------------------------

let data = {
name:name,
mobile:mobile,
email:email,
service:service,
message:message
};

try{

let response = await fetch("/api/leads",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
});

let result = await response.json();

// If backend sends error
if(!response.ok){
throw new Error(result.error || "Something went wrong");
}

// Success
Swal.fire({
icon:'success',
title:'Thank You 🎉',
text:'Our Team Will Contact You Soon',
confirmButtonColor:'#00aaff'
});

document.querySelector("form").reset();

}catch(error){

Swal.fire({
icon:'error',
title:'Error',
text:error.message
});

}

}