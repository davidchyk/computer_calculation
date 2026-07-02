#include "gui.h"

static char* get_html(void) {

    #ifdef _WIN32

        return "file:///C:/Users/artem/Desktop/Workspace/Projects/computer_calculation/srcC/gui/frontend/index.html";

    #else

        return "";

    #endif

}

int gui_run(void) {

    webview_t main_window = webview_create(0, NULL);

    webview_set_title(main_window, "Computer Calculation Program");

    webview_set_size(main_window, 800, 600, WEBVIEW_HINT_MIN);
    webview_set_size(main_window, 800, 600, WEBVIEW_HINT_FIXED);

    webview_navigate(main_window, get_html());

    webview_run(main_window);
    webview_destroy(main_window);

    return 0;

}
