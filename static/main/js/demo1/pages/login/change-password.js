"use strict";

// Class Definition
var KTLoginGeneral = function () {

    var showErrorMsg = function (form, type, msg) {
        var alert = $('<div class="kt-alert kt-alert--outline alert alert-' + type + ' alert-dismissible" role="alert">\
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">&nbsp;&nbsp;<i class="fa fa-times"></i></button><span></span></div>');

        form.find('.alert').remove();
        alert.prependTo(form);
        //alert.animateClass('fadeIn animated');
        KTUtil.animateClass(alert[0], 'fadeIn animated');
        alert.find('span').html(msg);
    }


    var handleForgotNewFormSubmit = function () {
        $('#kt_login_forgot_new').click(function (e) {
            e.preventDefault();

            var btn = $(this);
            var form = $(this).closest('form');

            form.validate({
                rules: {
                    password: {
                        required: true,
                        minlength: 8
                    },
                    rpassword: {
                        required: true,
                        minlength: 8,
                        equalTo: "#password"
                    },
                }
            });

            if (!form.valid()) {
                return;
            }

            btn.addClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', true);

            form.ajaxSubmit({
                url: '{{ request.path }}',
                type: 'post',
                success: function (response, status, xhr, $form) {
                    setTimeout(function () {
                        btn.removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false); // remove
                        form.clearForm(); // clear form
                        form.validate().resetForm(); // reset validation states

                        showErrorMsg(form, 'success', 'Cool! Your password has been updated!');
                    }, 2000);
                    setTimeout(function () {
                        window.location.replace('/')
                    }, 1000);
                }
            });
        });
    }


    // Public Functions
    return {
        // public functions
        init: function () {
            handleForgotNewFormSubmit();
        }
    };
}();

// Class Initialization
jQuery(document).ready(function () {
    KTLoginGeneral.init();
});