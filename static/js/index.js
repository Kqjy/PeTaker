interactiondiv = document.getElementById("interaction");
overview = document.getElementById("overview");
interactionbtns = document.getElementById("interaction-buttons");
petimage = document.getElementById("petimage");

function adoptPet() {
    if (document.getElementsByClassName("headlessui")[0])
    {
        return
    }
    var panel = document.createElement("div");
    panel.setAttribute("class","headlessui");
    var panelback = document.createElement("div");
    panelback.setAttribute("class","headlessui-back");
    var inpanel = document.createElement("div");
    inpanel.setAttribute("class","some-form")
    var form = document.createElement("form");
    form.method = "post";
    form.action = "/actions/adopt";
    form.id = "form-adopt";
    form.enctype = "application/json";
    var paneltitle = document.createElement("h3");
    paneltitle.textContent = "Adopt a Pet";
    paneltitle.style.textAlign = "center";
    var type = document.createElement("select");
    type.setAttribute("type","text");
    type.setAttribute("name","type");
    type.setAttribute("class","some-form-input some-form-select");
    pet_options = ["dog", "cat", "bird"];
    for (let catop = 0; catop < pet_options.length; catop++) {
        var option = document.createElement("option");
        option.setAttribute("value",pet_options[catop]);
        option.textContent = toTitleCase(pet_options[catop]);
        type.appendChild(option);
    }
    var typelabel = document.createElement("label");
    typelabel.textContent = "Type of Pet";
    var name = document.createElement("input");
    name.setAttribute("type","text");
    name.setAttribute("name","name");
    name.setAttribute("placeholder","Pet Name");
    name.setAttribute("maxlength", "100");
    name.setAttribute("class","some-form-input");
    var namelabel = document.createElement("label");
    namelabel.textContent = "Name of Pet";
    var submit = document.createElement("input");
    submit.setAttribute("type","submit");
    submit.setAttribute("value","Confirm");
    submit.setAttribute("class","some-form-button");
    submit.setAttribute("id","form-button-submit");
    var cancel = document.createElement("button");
    cancel.textContent = "Cancel";
    cancel.setAttribute("type","button");
    cancel.setAttribute("onclick","cancelform()");
    cancel.setAttribute("class","some-form-button");
    var div_panelbot = document.createElement("div");
    div_panelbot.appendChild(cancel);
    div_panelbot.appendChild(submit);
    form.appendChild(paneltitle);
    form.appendChild(typelabel); 
    form.appendChild(type);
    form.appendChild(namelabel);
    form.appendChild(name);
    form.appendChild(div_panelbot);
    inpanel.appendChild(form);
    panel.appendChild(inpanel);
    panelback.appendChild(panel);
    document.body.appendChild(panelback);
    document.body.setAttribute("style", "overflow: hidden;");

let someform = document.querySelector("#form-adopt");
someform.addEventListener("submit", function(event){
    event.preventDefault();
    document.getElementById("form-button-submit").enabled = false;
    const formData = new FormData(event.target);
    fetch(someform.action, {
        method: "post",
        body: JSON.stringify(Object.fromEntries(formData))
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        return response.text().then((text) => {throw Error(text['error'])});
    }).then((data) => {       
        console.log(data) 
        cancelform();     
        RefreshDashboard();
        RaiseOverview(data);
    }).catch((error) => {
        console.log(error)
        cancelform();
        RaiseOverview(error);
    });
    });
}

function viewPet() {
    const data = {};
    fetch("/actions/view", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.json();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        console.log(data);
        RefreshDashboard();
        RaiseOverview("Refreshed!");
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function feedPet() {
    const data = {};
    fetch("/actions/feed", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        RefreshDashboard();
        RaiseOverview(data);
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function washPet() {
    const data = {};
    fetch("/actions/wash", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        RefreshDashboard();
        RaiseOverview(data);
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function playPet() {
    const data = {};
    fetch("/actions/play", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        RefreshDashboard();
        RaiseOverview(data);
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function petPet() {
    const data = {};
    fetch("/actions/pet", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        throw new Error(response.statusText);
    }).then((data) => {   
        RaiseOverview(data);
        RefreshDashboard();
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function abandonPet(name) {
    const data = { "name": name.value };
    fetch("/actions/abandon", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.text();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        RefreshDashboard();
        RaiseOverview(data);
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function logsPet() {
    fetch("/api/logs", {
        method: "post",
        body: JSON.stringify({}),
    }).then((response) => {
        if (response.ok) {
        return response.json();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        RefreshDashboard();
        getlogs = document.getElementById("logscontent");
        if (getlogs) {
            getlogs.remove();
        }
        var div = document.createElement("div");
        var title = document.createElement("p");
        div.setAttribute("id", "logscontent");
        title.textContent = "=== LOGS ===";
        div.appendChild(title);
        for (let i in data) {
            var p = document.createElement("p");
            p.textContent = `[${data[i]['timestamp']}] ${data[i]['details']}`;
            div.appendChild(p);
        }
        setTimeout(function(){
            div.remove();
        }, 8000);
        interactiondiv.after(div);     
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function RefreshDashboard() {
    const data = {};
    fetch("/api/view", {
        method: "post",
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.ok) {
        return response.json();
        }
        throw new Error(response.statusText);
    }).then((data) => {
        overview.innerHTML = "";
        interactionbtns.innerHTML = "";
        if (data === undefined || data.length == 0) 
        {
            petimage.src = "/static/images/emptyspace.png";
            var para = document.createElement('p');
            para.textContent = "Try adopting a pet today!";
            var button = document.createElement('button');
            button.textContent = "Adopt";
            button.setAttribute("onclick", "adoptPet()");
            interactionbtns.appendChild(button);
            overview.appendChild(para);
        }
        else {
            var name = document.createElement('p');
            var para = document.createElement('p');  
            name.textContent = `Name: ${data[0]['name']} (Level ${data[0]["stats"]["level"]}: ${data[0]["stats"]["exp"]} EXP)`;
            for (let item in data[0]['status']) {
                para.textContent += toTitleCase(item) + ": " + data[0]['status'][item] + "/100 ";
            }
            overview.appendChild(name);
            overview.appendChild(para);

            petimage.src = "/static/images/" + data[0]["type"] + "0001.png";

            button_list = ["view", "feed", "wash", "play", "pet", "logs", "abandon"]
            for (let op = 0; op < button_list.length; op++) {
                var button = document.createElement('button');
                button.setAttribute("onclick",button_list[op] + "Pet()");
                button.textContent = toTitleCase(button_list[op]);
                if (button_list[op] === "abandon") {
                    button.setAttribute("class","danger");
                    button.setAttribute("onclick",button_list[op] + "Pet(this)");
                    button.setAttribute("value", data[0]['name'])
                }
                interactionbtns.appendChild(button);
            }
        }
    }).catch((error) => {
        console.log(error)
        RaiseOverview(error);
    });
}

function RaiseOverview(message) {
    var para = document.createElement('p');
    para.textContent = message;
    getnoti = document.getElementById("notification");
    if (getnoti)
    {
        getnoti.prepend(para);
    }
    else
    {
        noti = document.createElement("div");
        noti.setAttribute("id","notification"); 
        noti.appendChild(para);
        interactiondiv.insertBefore(noti, overview);
    }
    setTimeout(function(){
        para.remove();
        if (document.getElementById("notification").innerHTML === "") {
            document.getElementById("notification").remove();
        }
    }, 5000);
}

function toTitleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return (word.charAt(0).toUpperCase() + word.slice(1));
    }).join(' ');
  }

function cancelform() {
    document.getElementsByClassName("headlessui-back")[0].remove();
    document.body.setAttribute("style", "");
}

window.addEventListener("focus", function(event) 
{ 
    RefreshDashboard();
}, false);