# Auth Skip |  AngstromCTF 2022


Pour commencer nous avons la source du service web en place.

C'est du nodeJS avec comme Framework **ExpressJS**.
```JS
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");

const app = express();
const port = Number(process.env.PORT) || 8080;

const flag = process.env.FLAG || "actf{placeholder_flag}";

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.post("/login", (req, res) => {
    if (
        req.body.username !== "admin" ||
        req.body.password !== Math.random().toString()
    ) {
        res.status(401).type("text/plain").send("incorrect login");
    } else {
        res.cookie("user", "admin");
        res.redirect("/");
    }
});

app.get("/", (req, res) => {
    if (req.cookies.user === "admin") {
        res.type("text/plain").send(flag);
    } else {
        res.sendFile(path.join(__dirname, "index.html"));
    }
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}.`);
});
```

## Exploitation 

Nous allons nous intéresser à la route avec la méthode GET qui est à la racine du service.
Comme toute route, elle prend deux paramêtres une *Request* & une *Response* *(req,res)*.

```js
app.get("/", (req, res) => {
    if (req.cookies.user === "admin") {
        res.type("text/plain").send(flag);
    } else {
        res.sendFile(path.join(__dirname, "index.html"));
    }
});
`````

On voit donc que si nous mettons dans notre Requête des cookie **"user"** qui ont pour valeur **"admin"**.
Alors nous recevons le flag pour valider le challenge.

![](https://i.ibb.co/LppfDHq/chall.png)
Nous n'avons plus qu'à actualiser et nous aurons le flag.

    actf{passwordless_authentication_is_the_new_hip_thing}


