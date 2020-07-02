/* JS for products page */

// set array of selectors we want to match heights for:
var selectors = ['.tutorial-head'];

//on ready function
$(document).ready(function () {
    // initial alignment
    alignItems(selectors);
    // add listener if user changes size of window/viewport
    window.addEventListener('resize', function () {
        alignItems(selectors);
    });
});


