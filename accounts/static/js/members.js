/*
    KEY COMPONENTS:
    "member_list" = Will contain previous state of list of members.

    PROCESS:
    1 - User fills in Member form: Email
    2 - User Submits Member (clicks Add button)
    3 - Ajax sent to verify form and get user pk if email is in system
    4 - store as JSON string in members hidden input
    5 - build HTML for display in members_list

 */


/* when page loads due to potential errors in create form, should check for members */
member_list();
var max_members = parseInt(document.getElementById('max_members').value);

/* helper function to get list of members */
function get_members() {
    // hidden input containing members that is sent with Create Challenge post
    var list = document.getElementById('id_members').value;
    if (list != null && list !== "") {
        list = JSON.parse(list);
    } else {
        list = []
    }
    return list;
}

/* helper function to get list of original members */
function orig_member_list() {
    var orig_members = document.getElementById('id_orig_members').value;
    if (orig_members != null && orig_members !== "") {
        orig_members = JSON.parse(orig_members);
    } else {
        orig_members = []
    }
    return orig_members;
}


/* create HTML for list of members for UI */
function member_list() {
    // members html output container
    var update = false;
    try {
        update = document.getElementById("update").value;
    } catch (e) {
        update = false
    }
    var list = get_members();
    var user = document.getElementById("id_user").value;
    var member_block = document.getElementById('member_list');
    member_block.innerHTML = '';
    for (var i in list) {

        if (list[i].email !== user) {
            var item = `
                <div id="member-row-${list[i].email}" class="row member-row">            
                    <div class="form-group col-9 mb-0">
                      <div class="member">${list[i].email}</div>
                    </div>            
                    <div class="form-group col-3 mb-0">
                      <div class="form-group">
                         <a onclick="remove('${list[i].email}');" class="form-control btn btn-primary"><i class="fas fa-user-times"></i> Remove</a>
                      </div>
                    </div>
                </div>
                `;
            member_block.innerHTML += item;
        }
    }

}


/* Remove Member from list */
function remove(email) {
    var list = get_members();

    list = $.grep(list, function (e) {
        return e.email != email;
    });
    document.getElementById('id_members').value = JSON.stringify(list);
    max_member_messaging();
    member_list();

}


/* send request out to validate Member Form and to then add result to  member_list */
function add_member() {
    var list = get_members();
    var orig_members = orig_member_list();
    var user = document.getElementById("id_user").value;
    // if exceeds max members, ignore input
    if (list.length < max_members) {

        //pull email from input
        var email = document.getElementById('email').value;
        //make sure it's valid first
        if (ValidateEmail(email)) {

            // Check that email is not already in list
            var emailInList = objectPropInArray(list, 'email', email);
            var emailInOrig = objectPropInArray(orig_members, 'email', email);
            // add it to the list if it's not in there already

            if (!emailInList && !emailInOrig && email !== user) {

                //stuff result into list
                list.push({
                    'email': email,
                });
                // set CreateChallengeFrom members value
                document.getElementById('id_members').value = JSON.stringify(list);
                //clear out entry forms
                document.getElementById('email').value = '';
                // update list displayed on page
                member_list();
            } else {
                //email already in list
                document.getElementById('email').focus();
                document.getElementById('email').classList.add('is-invalid');
                document.getElementById('error_email').classList.add('invalid-feedback');
                document.getElementById('error_email').innerHTML = '<strong>You already have this email address in the list.</strong>';
            }
        }
    }
    // see if messaging needs to be shown
    max_member_messaging();
}

/* helper function to hide show max member messaging */
function max_member_messaging() {
    var list = get_members();

    var add_btn = document.getElementById('add_member');
    var mem_list_errs = document.getElementById('member_list_errors');
    var err_mem_list = document.getElementById('error_member_list');
    var member_inputs = document.getElementsByClassName('member-entry');

    if (list.length >= max_members) {
        add_btn.classList.add('is-disabled');
        add_btn.setAttribute('disabled', true);
        mem_list_errs.classList.add('is-invalid');
        err_mem_list.classList.add('invalid-feedback');
        err_mem_list.innerHTML = '<strong>You have reached the max number of members for your family.</strong>';
        err_mem_list.style.display = "block";
        Array.prototype.forEach.call(member_inputs, function (item) {
            item.style.display = "none";
            if (item.classList.contains('d-none')) {
                item.classList.remove('d-md-block');
            }
        });

    } else {
        add_btn.classList.remove('is-disabled');
        add_btn.setAttribute('disabled', false);
        mem_list_errs.classList.remove('is-invalid');
        err_mem_list.classList.remove('invalid-feedback');
        err_mem_list.innerHTML = '';
        err_mem_list.style.display = "none";
        Array.prototype.forEach.call(member_inputs, function (item) {
            item.style.display = "block";
            if (item.classList.contains('d-none')) {
                item.classList.add('d-md-block');
            }
        });
    }
}


/* Helper Function to check if an array of dictionaries has a property of a certain value */
function objectPropInArray(list, prop, val) {
    try {
        if (list.length > 0) {
            for (i in list) {
                if (list[i][prop] === val) {
                    return true;
                }
            }
        }
        return false;
    } catch (e) {
        return false;
    }
}

/* validate email address input field */
function ValidateEmail(value) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (value.match(mailformat)) {
        document.getElementById('email').classList.remove('is-invalid');
        document.getElementById('error_email').classList.remove('invalid-feedback');
        document.getElementById('error_email').innerHTML = '';
        return true;
    } else {
        document.getElementById('email').focus();
        document.getElementById('email').classList.add('is-invalid');
        document.getElementById('error_email').classList.add('invalid-feedback');
        document.getElementById('error_email').innerHTML = '<strong>Please enter a valid email address.</strong>';
        return false;
    }
}


