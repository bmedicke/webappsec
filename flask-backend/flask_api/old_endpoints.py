# @app.route("/u/<user_id>")
# def user_profile(user_id):
#     """
#     user profile page
#     """
#     return f"{escape(user_id)}'s profile"

# @app.route("/e/<escaped>")
# def no_injection(escaped):
#     """
#     injection-safe demo route

#     localhost:7701/e/<body onload='alert("this is bad");'>
#     """
#     return f"{escape(escaped)}"

# @app.route("/i/<unescaped>")
# def injection(unescaped):
#     """
#     injection demo route

#     localhost:7701/i/<body onload='alert("this is bad");'>
#     """
#     return f"{unescaped}"
