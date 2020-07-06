// document ready, add listeners
document.addEventListener("DOMContentLoaded", () => {
    // handler for switch family dropdown
    document.getElementById('switch_family').addEventListener("change", (e) => {
        window.location = "/accounts/get_family/" + e.target.value;
    });

    // add a listener to update_status form submit button
    let from = document.getElementById('update_status');
    from.addEventListener('submit', function (e) {
        e.preventDefault();
        // submit new status to API URL
        update_status();
    });

});

function update_status() {
    // make sure button isn't disabled because of throttling
    let button = document.getElementById('update-status-submit');
    if (button.classList.contains('disabled')) {
        return false;
    }

    // Clean out any errors and error messages
    document.querySelectorAll('.field-error').forEach(el => {
        while (el.firstChild) {
            el.removeChild(el.firstChild);
        }
    });

    // get user's mood from the form
    let mood = false;
    document.getElementsByName("mood").forEach(el => {
        if (el.checked) {
            mood = el.value;
        }
    });
    // mood has to be selected to submit, so if no value, return back with error message
    if (!mood) {
        document.querySelector('#id_mood_error').innerHTML = "Please select how you are feeling.";
        document.querySelector('#id_mood').classList.add('has-error');
        return false
    }

    // get user's plans
    let plans = document.getElementById('id_plans').value;
    if (plans.length === 0) {
        plans = "Nothing"
    }

    //get user's help
    let help = document.getElementById('id_help').value;
    if (help.length === 0) {
        help = "Nothing"
    }

    //get user_id
    let user = document.getElementById('id_user').value;

    //get family_id
    let family = document.getElementById('id_family').value;


    //get the CSRF_TOKEN
    let csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // send request to update status
    let url = '/status/send_status/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'mood': mood,
            'plans': plans,
            'help': help,
            'user_id': user,
            'family_id': family,
        })
    })
        .then(response => response.json())
        .then(data => {
                // See if errors coming back
                if ('errors' in data) {
                    //have an error,
                    for (let key in data.errors) {
                        document.querySelector('#id_' + key + '_error').innerHTML = data.errors[key][0];
                        document.querySelector('#' + key).classList.add('has-error');
                    }

                } else if ('message' in data) {
                    if (data['message'] === 'rate limit exceeded') {
                        let item = ` <div id="data-row-error" class="form-group has-error">
                                        <div class="has-error">
                                            We're sorry, you have reached the limit of status updates for the day. Please try again tomorrow.
                                        </div>
                                      </div>
                                    </div>
                              `;
                        button.classList.add('disabled');

                    }
                } else {
                    // success from send_update API request does nothing to current user's screen. Get all status happens on a timer.

                }
            }
        )
        .catch((error) => {
            console.log('Got an error')
        });

}