url_params = new URLSearchParams(document.location.search)

const user_name = url_params.get("name")
const user_email = url_params.get("email")
const user_description = url_params.get("description")
const user_password = url_params.get("password")

const user = {
	"name": user_name,
	"email": user_email,
	"password": user_password,
	"description": user_description,
}

if (JSON.parse(core.cookies.get("user")) !== user) {
	core.cookies.set("user", JSON.stringify(user))
}


const forum = {
    openContent: function (contentId) {
        for (var i = 0; i in document.getElementsByClassName("content-item"); i++) {
            document.getElementsByClassName("content-item")[i].style.display = "none"
        }
        for (var i = 0; i in document.getElementsByClassName("content-button"); i++) {
            document.getElementsByClassName("content-button")[i].classList.remove("content-button-active")
        }
        document.getElementById("content-" + contentId).style.display = "grid"
        if (document.getElementById("button-" + contentId)) {
            document.getElementById("button-" + contentId).classList.add("bold")
            document.getElementById("button-" + contentId).classList.add("content-button-active")
        }
    },
    openFrame: function (frameURL) {
        this.openContent("frame")
        document.getElementById("frame-main").src = frameURL
        document.getElementById("frame-back").addEventListener("click", function () {
            document.getElementById("content-frame").style.display = "none"
            forum.openContent("homepage")
        })
    },
	
    alert: function (message, onclick) {
        document.getElementById("alert").style.display = "grid"
        document.getElementById("alert-contents").innerText = message
        document.getElementById("alert-contents").addEventListener("click", function () {
            document.getElementById("alert").style.display = "none"
            onclick()
        })
        document.getElementById("alert-close").addEventListener("click", function () {
            document.getElementById("alert").style.display = "none"
        })
    },

    getProfile: function () {
        document.getElementById("content-profile-header").innerHTML = "<h1>" + user.name + "</h1><p>" + user.description + "</p>"
    },
    getUsers: async function () {
        shuffle = (list) => list.sort(() => Math.random() - 0.5);

        f = await fetch("/api/get_users")
        f = await f.json()
        f = shuffle(f)

        parent_element = document.getElementById("content-active-items")
        parent_element.innerHTML = "<h1>Active</h1><p>This is a list of users who are online or have been online recently.</p>"
        for (var i = 0; i < f.length; i++) {         
            parent = document.createElement("div")   
            parent.innerHTML = `<p>${f[i].name} <b>${f[i].description}</b></p>`
            parent_element.appendChild(parent)
            var name = f[i].name
            parent.addEventListener("click", function () {
                forum.openFrame("/profile/" + name)
            })
        }
    },

    createPost: async function (text, name, email, password) {
        try {
            var f = await fetch(`/api/add_post?text=${text}&name=${name}&email=${email}&password=${password}`)
            f = await f.json()
            return true
        } catch (e) {
            console.log(e)
            return false
        }
    },
    getFeed: async function () {
        var f = await fetch("/api/get_feed")
        f = await f.json()
        document.getElementById("feed").innerHTML = ""
        for (var i = 0; i < f.length; i++) {
            document.getElementById("feed").innerHTML+=`<div><b>${f[i].author}</b><i>${f[i].date}</i><p>${f[i].text}</p></div>`
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    forum.getProfile()
    forum.getFeed()
    forum.getUsers()

    setInterval(function () {
        forum.getProfile()
    }, 20000)
    setInterval(function () {
        forum.getUsers()
    }, 5000)
    setInterval(function () {
        forum.getFeed()
    }, 2000)

    document.getElementById("post-submit").addEventListener("click", async function () {
        var user = JSON.parse(core.cookies.get("user"))
        forum.alert("Post being submitted...")
        await forum.createPost(document.getElementById("post-input").innerText, user.name, user.email, user.password)
        forum.alert("Post successfully submitted")
        forum.getFeed()
        document.getElementById("post-input").innerText = ""
    })
})