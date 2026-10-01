const API = window.location.origin;

async function api(url, options = {}) {
    const { method = "GET", params = {} } = options;
    const query = new URLSearchParams(params).toString();

    const response = await fetch(
        API + url + (query ? "?" + query : ""),
        { method: method }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
    }

    return data;
}

async function login() {
    let username = sessionStorage.username;
    let password = sessionStorage.password;

    if (!username || !password) {
        username = prompt("Username:");
        password = prompt("Password:");

        if (!username || !password) {
            return false;
        }
    }

    try {
        const result = await api("/login", {
            method: "POST",
            params: {
                username: username,
                password: password
            }
        });

        if (
            result.message !== "Login successful" &&
            result.message !== "Register successful"
        ) {
            sessionStorage.clear();
            alert("Incorrect username or password.");
            return false;
        }

        sessionStorage.username = username;
        sessionStorage.password = password;

        return true;
    } catch (error) {
        sessionStorage.clear();
        alert(error.message);
        return false;
    }
}

async function getPosts() {
    return (await api("/data")).data;
}

function displayPosts(posts) {
    const container = document.getElementById("posts-container");

    if (!container) return;

    container.innerHTML = "";

    if (!posts.length) {
        container.textContent = "No posts found.";
        return;
    }

    for (let i = 0; i < posts.length; i++) {
        const post = posts[i];

        const box = document.createElement("div");
        box.className = "result-box";

        const title = document.createElement("h3");
        title.textContent = post[0];

        const description = document.createElement("p");
        description.textContent = post[1];

        const author = document.createElement("p");
        author.className = "post-user";
        author.textContent = "Posted by " + post[2];

        box.append(title, description, author);

        box.onclick = function () {
            location.href =
                "pages/post.html?heading=" +
                encodeURIComponent(post[0]);
        };

        container.appendChild(box);
    }
}

async function search() {
    const input = document.getElementById("search-input");
    const container = document.getElementById("posts-container");

    const query = input.value.trim();

    if (!query) {
        container.innerHTML = "";
        return;
    }

    try {
        const posts = (
            await api("/search/" + encodeURIComponent(query))
        ).data;

        displayPosts(posts);
    } catch (error) {
        container.textContent = error.message;
    }
}

async function togglePosts() {
    const container = document.getElementById("posts-container");
    const button = document.getElementById("see-all-button");

    if (container.children.length) {
        container.innerHTML = "";
        button.innerHTML = "<b>=</b> See All";
        return;
    }

    try {
        displayPosts(await getPosts());
        button.innerHTML = "<b>=</b> Hide All";
    } catch (error) {
        container.textContent = error.message;
    }
}

function setupHome() {
    const form = document.getElementById("search-form");
    const seeAll = document.getElementById("see-all-button");

    if (!form) return;

    form.onsubmit = function (event) {
        event.preventDefault();
        search();
    };

    if (seeAll) {
        seeAll.onclick = togglePosts;
    }
}

async function setupPost() {
    const container = document.getElementById("post-container");

    if (!container) return;

    const heading = new URLSearchParams(location.search).get("heading");

    if (!heading) {
        container.textContent = "Post not found.";
        return;
    }

    try {
        const posts = await getPosts();

        let post = null;

        for (let i = 0; i < posts.length; i++) {
            if (posts[i][0] === heading) {
                post = posts[i];
                break;
            }
        }

        if (!post) {
            container.textContent = "Post not found.";
            return;
        }

        container.innerHTML = "";

        const title = document.createElement("h1");
        title.textContent = post[0];

        const content = document.createElement("div");
        content.className = "post-content";
        content.textContent = post[1];

        const author = document.createElement("p");
        author.className = "post-user";
        author.textContent = "Posted by " + post[2];

        container.append(title, content, author);

        const editButton = document.getElementById("edit-button");
        const deleteButton = document.getElementById("delete-button");

        if (editButton) {
            editButton.onclick = function () {
                location.href =
                    "create.html?edit=" +
                    encodeURIComponent(post[0]);
            };
        }

        if (deleteButton) {
            deleteButton.onclick = async function () {
                if (!confirm("Delete this post?")) return;

                if (!await login()) return;

                try {
                    await api("/delete", {
                        method: "POST",
                        params: {
                            username: sessionStorage.username,
                            password: sessionStorage.password,
                            heading: post[0]
                        }
                    });

                    location.href = "../index.html";
                } catch (error) {
                    alert(error.message);
                }
            };
        }
    } catch (error) {
        container.textContent = error.message;
    }
}

async function setupCreate() {
    const form = document.getElementById("post-form");

    if (!form) return;

    const params = new URLSearchParams(location.search);
    const edit = params.get("edit");

    if (edit) {
        document.getElementById("form-title").textContent = "Edit";
        document.getElementById("submit-button").textContent = "Save";

        try {
            const posts = await getPosts();

            let post = null;

            for (let i = 0; i < posts.length; i++) {
                if (posts[i][0] === edit) {
                    post = posts[i];
                    break;
                }
            }

            if (!post) {
                alert("Post not found.");
                return;
            }

            document.getElementById("title").value = post[0];
            document.getElementById("description").value = post[1];
        } catch (error) {
            alert(error.message);
            return;
        }
    }

    form.onsubmit = async function (event) {
        event.preventDefault();

        const title = document.getElementById("title").value.trim();
        const description =
            document.getElementById("description").value.trim();

        if (!title || !description) {
            alert("Please fill in both fields.");
            return;
        }

        if (!await login()) return;

        const user = {
            username: sessionStorage.username,
            password: sessionStorage.password
        };

        try {
            if (edit) {
                await api("/update", {
                    method: "POST",
                    params: {
                        username: user.username,
                        password: user.password,
                        heading: edit,
                        new_heading: title,
                        new_description: description
                    }
                });
            } else {
                await api("/upload", {
                    method: "POST",
                    params: {
                        username: user.username,
                        password: user.password,
                        heading: title,
                        description: description
                    }
                });
            }

            location.href =
                "post.html?heading=" + encodeURIComponent(title);
        } catch (error) {
            alert(error.message);
        }
    };
}

setupHome();
setupPost();
setupCreate();