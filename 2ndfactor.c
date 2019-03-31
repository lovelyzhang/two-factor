#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include "verify.h"


/* expected hook */
PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}

/* this function is ripped from pam_unix/support.c, it lets us do IO via PAM */
int converse(pam_handle_t *pamh, int nargs, struct pam_message **message, struct pam_response **response) {
    int retval;
    struct pam_conv *conv;

    retval = pam_get_item(pamh, PAM_CONV, (const void **) &conv);
    if (retval == PAM_SUCCESS) {
        retval = conv->conv(nargs, (const struct pam_message **) message, response, conv->appdata_ptr);
    }

    return retval;
}

/* expected hook, this is where custom stuff happens */
PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    int retval;
    char *input;
    struct pam_message msg[1], *pmsg[1];
    struct pam_response *resp;
    const char *username;
    if ((retval = pam_get_user(pamh, &username, "login: ")) != PAM_SUCCESS) {
        return retval;
    }

    if (0 == send_code(username)) {
        pmsg[0] = &msg[0];
        msg[0].msg_style = PAM_PROMPT_ECHO_OFF;
        msg[0].msg = "1-time code: ";
        resp = NULL;
        if ((retval = converse(pamh, 1, pmsg, &resp)) != PAM_SUCCESS) {
            return retval;
        }

        if (resp) {
            if ((flags & PAM_DISALLOW_NULL_AUTHTOK) && resp[0].resp == NULL) {
                free(resp);
                return PAM_AUTH_ERR;
            }
            input = resp[0].resp;
            resp[0].resp = NULL;
            if (0 == verify_code(username, input)) {
                free(input);
                free(resp);
                return PAM_SUCCESS;
            } else {
                free(input);
                free(resp);
                return PAM_AUTH_ERR;
            }
        } else {
            return PAM_AUTH_ERR;
        }
    }
    return PAM_SUCCESS;
}
