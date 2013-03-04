<?
function replace_url($url) {
    global $localhost;
    return str_replace($localhost,$_SERVER["SERVER_NAME"],$url);
}
