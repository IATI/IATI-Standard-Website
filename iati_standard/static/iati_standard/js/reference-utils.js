$(function() {

    $('#profile-data-controls').each(function() {
        var dataUrl = '/cms/iati_standard/update-profile-data/';
        var pollUrl = '/cms/iati_standard/get-update-progress/';
        var $updateButton = $('.action-update-profile-data');
        var $form = $('#page-edit-form');
        var controls = $(this);
        var message_list = controls.find('.messages ul');
        var updating = false;
        var pollTimeout = -1;
        var pollInterval = 1000;
        var taskId = null;

        // move so this is a direct child of the help container
        controls.appendTo(controls.closest('.help-block'));

        // request the profie data for the tag
        function requestProfileUpdate(tag) {

            // add the requested tag field name to the form
            var data = new FormData($form[0]);
            data.append('tag-to-update', tag);

            // get and return the data
            return $.ajax({
                url: dataUrl,
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
            });
        }

        // click handler for the update buttons
        $updateButton.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            // return if there's an update running
            if (updating) {
                return;
            }

            // set update status and clear messages
            updating = true;
            removeMessages();

            // replicate long running button functionality (can't use wagtail admin as it resets after 30 seconds)
            var $self = $(this);
            var $replacementElem = $('em', $self);
            $self.data('original-text', $replacementElem.text());
            $replacementElem.text($self.data('clicked-text'));
            $self.addClass('button-longrunning-active').prop('disabled', 'true');

            // make the request and handle response states
            requestProfileUpdate($self.data('tag')).done(function (data) {
                if (data['is_valid']) {
                    taskId = data.task_id;
                    addMessage('Data transfer started', data.message_class);
                    pollProgress();
                } else {
                    addMessage(data.error, data.message_class);
                    onEnd();
                }
            }).fail(function () {
                addMessage('Error transferring data', 'error');
            });

            // reset the button
            function cancelSpinner() {
                $self.prop('disabled', '').removeClass('button-longrunning-active');
                $replacementElem.text($self.data('original-text'));
            };

            // ajax poll for progress
            function requestPollProgress() {

                // add the task_id to the form
                var data = new FormData($form[0]);
                data.append('task_id', taskId);

                return $.ajax({
                    url: pollUrl,
                    method: 'POST',
                    data: data,
                    processData: false,
                    contentType: false,
                });
            };

            // start poll for progress
            function pollProgress() {

                clearTimeout(pollTimeout);

                // make the poll request and handle response states
                requestPollProgress().done(function (data) {
                    if (data.state == 'SUCCESS') {
                        onEnd();
                        addMessage('Data transfer complete', 'success');
                    }
                    else if (data.state == 'PROGRESS') {
                        addNewMessage(data.info, 'success');
                        pollTimeout = setTimeout(pollProgress, pollInterval);
                    }
                    else if (data.state == 'FAILURE') {
                        addNewMessage(data.info, data.message_class);
                        onEnd();
                    }
                    else if (data.state != 'PENDING') {
                        addNewMessage(data.state + ': ' + data.info, data.message_class);
                        pollTimeout = setTimeout(pollProgress, pollInterval);
                    }
                    else {
                        pollTimeout = setTimeout(pollProgress, pollInterval);
                    }
                }).fail(function () {
                    addMessage('An unrecoverable error has occurred - please contact the website admin for help.', 'error');
                    onEnd();
                }).always(function () {
                });
            };

            // called on success or failure
            function onEnd() {
                updating = false;
                cancelSpinner();
            }
        });

        // remove all response messages
        function removeMessages() {
            message_list.empty();
        }

        // add a response message
        function addMessage(message, message_class) {
            $('<li>' + message + '</li>').appendTo(message_list).addClass(message_class);
        }

        // add a response message
        function addNewMessage(message, message_class) {
            var lastMessage = message_list.find('li').last().text();
            if (message != lastMessage) {
                addMessage(message, message_class);
            }
        }
    });

});
