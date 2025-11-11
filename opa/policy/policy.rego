package http.authz

default allow = false

# Admins (Authenticated + admin) can GET and POST for users API
allow if {
    input.role == "admin"
    input.method in {"GET", "POST"}
    input.path in {"/api/users", "/api/users/"}
}

# Authenticated users can only GET users
allow if {
    input.sub != null
    input.sub != ""
    input.method == "GET"
    input.path in {"/api/users", "/api/users/"}
}

# Everyone else denied (default rule already handles this)
