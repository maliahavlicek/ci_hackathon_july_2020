// document ready, add listeners
document.addEventListener("DOMContentLoaded", () => {
    // handler for switch family dropdown
    document.getElementById('switch_family').addEventListener("change", (e) => {
        window.location = "/accounts/get_family/" + e.target.value;
    });

});